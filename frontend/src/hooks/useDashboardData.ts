import { useState, useEffect, useMemo } from 'react';
import axios from 'axios';
import type { Video, DailyStat, Timeframe, DateRange } from '../types';

interface ChannelStats {
    subscribers: number;
    views: number;
    videos: number;
    title: string;
    avatar: string;
}

export function useDashboardData(timeframe: Timeframe, activeMetric: 'views' | 'likes' | 'comments' | 'subscribers', customRange?: DateRange) {
    const [videos, setVideos] = useState<Video[]>([]);
    const [analytics, setAnalytics] = useState<DailyStat[]>([]);
    const [channelStats, setChannelStats] = useState<ChannelStats | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [analyticsMissing, setAnalyticsMissing] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                setError(null);
                // Use env var or default to relative path (handled by Nginx/Vite proxy)
                const apiBase = import.meta.env.VITE_API_URL || '/api';

                // Handle Auth Redirect Params
                const params = new URLSearchParams(window.location.search);
                if (params.get('auth_success') === 'true' && params.get('channel_id')) {
                    const newChannelId = params.get('channel_id')!;
                    localStorage.setItem('yt_channel_id', newChannelId);
                    // Clear URL
                    window.history.replaceState({}, '', window.location.pathname);
                }

                // Header Logic for Dynamic Channel
                // If viewing a specific channel (public link), use that.
                // Otherwise fallback to the logged-in user's channel.
                const viewingId = localStorage.getItem('yt_viewing_id');
                const loggedInId = localStorage.getItem('yt_channel_id');
                const targetId = viewingId || loggedInId;

                const apiKey = localStorage.getItem('yt_api_key');

                const headers: Record<string, string> = {};
                if (targetId) headers['x-youtube-channel-id'] = targetId;
                if (apiKey) headers['x-youtube-api-key'] = apiKey;

                const results = await Promise.allSettled([
                    axios.get(`${apiBase}/videos`, { headers, timeout: 15000 }),
                    axios.get(`${apiBase}/analytics`, { headers, timeout: 15000 }),
                    axios.get(`${apiBase}/channel`, { headers, timeout: 15000 })
                ]);

                const [videosRes, analyticsRes, channelRes] = results;

                // Handle Videos
                if (videosRes.status === 'fulfilled' && Array.isArray(videosRes.value.data)) {
                    setVideos(videosRes.value.data);
                } else {
                    console.warn("Videos fetch failed", videosRes);
                }

                // Handle Analytics
                if (analyticsRes.status === 'fulfilled' && Array.isArray(analyticsRes.value.data) && analyticsRes.value.data.length > 0) {
                    setAnalytics(analyticsRes.value.data);
                    setAnalyticsMissing(false);
                } else {
                    console.warn("Analytics fetch failed or empty (likely no OAuth)", analyticsRes);
                    setAnalyticsMissing(true);
                }

                // Handle Channel Stats
                if (channelRes.status === 'fulfilled' && channelRes.value.data) {
                    const data = channelRes.value.data;
                    const stats = data.stats || {};
                    setChannelStats({
                        subscribers: stats.subscribers || 0,
                        views: stats.views || 0,
                        videos: stats.videos || 0,
                        title: data.channelTitle || 'Canal Desconocido',
                        avatar: data.avatar || ''
                    });
                }

            } catch (error: any) {
                console.error("Error fetching data:", error);
                setError(`Error de Conexión: No se pudo contactar con el backend. (${error.message})`);
            } finally {
                setLoading(false);
            }
        }
        fetchData();
    }, []);

    // --- Logic & Filtering ---
    const filteredData = useMemo(() => {
        if (!analytics.length) return { current: [], previous: [] };

        if (!analytics.length) return { current: [], previous: [] };

        let cutoff = new Date(); // Start date for current period
        let endCutoff = new Date(); // End date for current period
        let prevCutoff = new Date(); // Start date for previous period

        const now = new Date();

        if (timeframe === 'custom' && customRange?.start && customRange?.end) {
            // ... (keep custom logic or simplify similarly if needed, but 'custom' usually provides full dates)
            cutoff = new Date(customRange.start);
            endCutoff = new Date(customRange.end);
        } else {
            let daysToFilter = 30;
            if (timeframe === '7d') daysToFilter = 7;
            if (timeframe === '15d') daysToFilter = 15;
            if (timeframe === 'all') daysToFilter = 365 * 10;

            cutoff = new Date();
            cutoff.setDate(now.getDate() - daysToFilter);

            // Previous period
            prevCutoff = new Date(cutoff);
            prevCutoff.setDate(cutoff.getDate() - daysToFilter);
        }

        // Convert cutoffs to YYYY-MM-DD strings for safe comparison with d.day (which is YYYY-MM-DD)
        const toIsoDate = (d: Date) => d.toISOString().split('T')[0];
        const cutoffStr = toIsoDate(cutoff);
        const endCutoffStr = endCutoff ? toIsoDate(endCutoff) : null;
        const prevCutoffStr = toIsoDate(prevCutoff);

        const current = analytics.filter(d => {
            // d.day is "YYYY-MM-DD" string from backend
            if (timeframe === 'custom' && endCutoffStr) {
                return d.day >= cutoffStr && d.day <= endCutoffStr;
            }
            return d.day >= cutoffStr;
        });
        // Sort current for charts
        current.sort((a, b) => a.day.localeCompare(b.day));

        const previous = analytics.filter(d => {
            return d.day >= prevCutoffStr && d.day < cutoffStr;
        });

        return { current, previous };
    }, [analytics, timeframe]);

    const stats = useMemo(() => {
        const calc = (arr: DailyStat[]) => ({
            views: arr.reduce((acc, d) => acc + d.views, 0),
            likes: arr.reduce((acc, d) => acc + d.likes, 0),
            comments: arr.reduce((acc, d) => acc + d.comments, 0),
            subscribers: arr.reduce((acc, d) => acc + (d.subscribers || 0), 0),
        });

        const current = calc(filteredData.current);
        const previous = calc(filteredData.previous);

        const getDiff = (curr: number, prev: number) => {
            if (prev === 0) return 0;
            return ((curr - prev) / prev) * 100;
        };

        return {
            current,
            diffs: {
                views: getDiff(current.views, previous.views),
                likes: getDiff(current.likes, previous.likes),
                comments: getDiff(current.comments, previous.comments),
                subscribers: getDiff(current.subscribers, previous.subscribers),
            }
        };
    }, [filteredData]);

    // Aggregation for Month Table
    const monthlyStats = useMemo(() => {
        const months: Record<string, { month: string, views: number, likes: number, comments: number, subscribers: number }> = {};
        analytics.forEach(d => {
            const monthKey = d.day.substring(0, 7); // YYYY-MM
            if (!months[monthKey]) {
                months[monthKey] = { month: monthKey, views: 0, likes: 0, comments: 0, subscribers: 0 };
            }
            months[monthKey].views += d.views;
            months[monthKey].likes += d.likes;
            months[monthKey].comments += d.comments;
            months[monthKey].subscribers += (d.subscribers || 0);
        });
        return Object.values(months).sort((a, b) => b.views - a.views); // Sort by highest views
    }, [analytics]);

    const chartData = useMemo(() => {
        return filteredData.current.map(d => ({
            name: new Date(d.day).toLocaleDateString(undefined, { day: 'numeric', month: 'short' }),
            value: d[activeMetric], // Dynamic metric
            date: d.day
        }));
    }, [filteredData, activeMetric]);

    const bestDay = useMemo(() => {
        if (!filteredData.current.length) return undefined;
        // Careful with type safety here, activeMetric is strictly typed
        const best = filteredData.current.reduce((max, current) => max[activeMetric] > current[activeMetric] ? max : current);
        return { date: best.day, value: best[activeMetric], metric: activeMetric };
    }, [filteredData, activeMetric]);

    // Sort top videos by views for the sidebar (Always fixed sort)
    const topVideos = useMemo(() => {
        return [...videos].sort((a, b) => b.Vistas - a.Vistas);
    }, [videos]);

    return {
        videos,
        loading,
        error,
        stats,
        monthlyStats,
        chartData,
        bestDay,
        topVideos,
        channelStats,
        statusMessage: error ? error : (loading ? "Cargando datos..." : null),
        activeChannelId: localStorage.getItem('yt_channel_id') || 'Canal Principal',
        analyticsMissing
    };
}
