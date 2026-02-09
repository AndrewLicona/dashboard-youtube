import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { Activity, Play, ThumbsUp, TrendingUp, Users, RefreshCcw } from 'lucide-react'

import type { Timeframe, DateRange } from '../types'
import { useDashboardData } from '../hooks/useDashboardData'
import { Header } from '../components/layout/Header'
import { KpiCard } from '../components/stats/KpiCard'
import { GrowthChart } from '../components/charts/GrowthChart'
import { VideoList } from '../components/content/VideoList'
import { MonthChart } from '../components/stats/MonthChart'
import { MediaKit } from '../components/sponsorship/MediaKit'
import { DynamicFavicon } from '../components/common/DynamicFavicon'

export function DashboardView() {
    const { channelId } = useParams(); // Get ID from URL

    // Update localStorage if URL has an ID (Viewing specific channel)
    useEffect(() => {
        if (channelId) {
            localStorage.setItem('yt_viewing_id', channelId);
        }
    }, [channelId]);

    // UI State
    const [timeframe, setTimeframe] = useState<Timeframe>('all')
    const [customRange, setCustomRange] = useState<DateRange>({ start: null, end: null })
    const [expandContent, setExpandContent] = useState(false)
    const [showMediaKit, setShowMediaKit] = useState(false)
    const [activeMetric, setActiveMetric] = useState<'views' | 'likes' | 'comments' | 'subscribers'>('views')

    // Data Logic 
    const {
        videos,
        loading,
        error,
        stats,
        monthlyStats,
        chartData,
        bestDay,
        topVideos,
        channelStats,
        analyticsMissing
    } = useDashboardData(timeframe, activeMetric, customRange);

    return (
        <div className="min-h-screen bg-[#0F0F0F] text-white font-sans selection:bg-gamer-green/30">
            <div className="max-w-7xl mx-auto p-4 md:p-8">

                <Header
                    onOpenMediaKit={() => setShowMediaKit(true)}
                    channelName={channelStats?.title}
                    channelAvatar={channelStats?.avatar}
                />

                <DynamicFavicon />

                {/* --- STATUS NOTIFICATION BAR --- */}
                <div className="mb-6 flex flex-col md:flex-row gap-4 justify-between items-center bg-[#1A1A1A] border border-white/5 p-4 rounded-2xl animate-in fade-in">
                    <div className="flex items-center gap-3">
                        <div className={`w-3 h-3 rounded-full ${loading ? 'bg-yellow-500 animate-pulse' : error ? 'bg-red-500' : 'bg-green-500'}`} />
                        <span className="text-sm font-bold text-gray-400 uppercase tracking-wider">
                            {loading ? 'Sincronizando datos...' : error ? 'Error de Conexión' : 'Sistema Online'}
                        </span>

                        {!loading && !error && (
                            <button
                                onClick={async () => {
                                    try {
                                        const apiBase = import.meta.env.VITE_API_URL || '/api';
                                        const apiKey = localStorage.getItem('yt_api_key');
                                        const targetId = localStorage.getItem('yt_viewing_id') || localStorage.getItem('yt_channel_id');
                                        const headers: Record<string, string> = {};
                                        if (targetId) headers['x-youtube-channel-id'] = targetId;
                                        if (apiKey) headers['x-youtube-api-key'] = apiKey;

                                        await axios.post(`${apiBase}/refresh`, {}, { headers });
                                        window.location.reload();
                                    } catch (e) {
                                        alert("Error al refrescar datos.");
                                    }
                                }}
                                className="ml-2 p-1 text-gray-500 hover:text-white transition-colors"
                                title="Forzar Actualización de Datos"
                            >
                                <RefreshCcw size={14} />
                            </button>
                        )}
                    </div>

                    {!analyticsMissing && channelStats?.title && (
                        <div className="flex items-center gap-2 px-3 py-1 bg-green-500/10 border border-green-500/20 rounded-lg">
                            <span className="text-[10px] text-green-500 font-bold uppercase tracking-wider">
                                Conectado: {channelStats.title}
                            </span>
                        </div>
                    )}

                    {analyticsMissing && !loading && !error && (
                        <a
                            href="http://localhost:8000/api/auth/login"
                            className="flex items-center gap-2 px-4 py-2 bg-yellow-500 hover:bg-yellow-400 text-black border border-yellow-500 rounded-xl transition-all cursor-pointer"
                        >
                            <div className="w-2 h-2 bg-black rounded-full animate-pulse" />
                            <span className="text-xs font-bold uppercase tracking-widest leading-none">
                                Conectar Canal de YouTube
                            </span>
                        </a>
                    )}
                </div>

                {/* --- TIMEFRAME FILTER BAR --- */}
                <div className="mb-8 flex flex-wrap justify-center items-center gap-2 bg-gamer-card p-2 rounded-2xl border border-gamer-border">
                    {(['7d', '15d', '30d', 'all', 'custom'] as Timeframe[]).map((t) => {
                        if (t === 'custom' && timeframe === 'custom') return null;
                        return (
                            <button
                                key={t}
                                onClick={() => setTimeframe(t)}
                                className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${timeframe === t ? 'bg-gamer-green text-black' : 'text-gray-500 hover:text-white'
                                    }`}
                            >
                                {t === 'all' ? 'Todo' : t === 'custom' ? 'Personalizado' : t}
                            </button>
                        )
                    })}

                    {timeframe === 'custom' && (
                        <div className="flex items-center gap-3 animate-in fade-in slide-in-from-right duration-300 bg-black/20 px-3 py-1 rounded-xl border border-white/5">
                            <div className="flex flex-col gap-0.5">
                                <span className="text-[8px] text-gray-500 font-bold uppercase tracking-wider ml-1">Desde</span>
                                <input
                                    type="date"
                                    value={customRange.start ? customRange.start.toISOString().split('T')[0] : ''}
                                    onChange={(e) => setCustomRange({ ...customRange, start: e.target.value ? new Date(e.target.value) : null })}
                                    className="bg-[#1A1A1A] border border-white/10 rounded-lg px-2 py-1 text-[10px] text-white focus:outline-none focus:border-gamer-green"
                                />
                            </div>

                            <div className="h-6 w-px bg-white/10 mt-3" />

                            <div className="flex flex-col gap-0.5">
                                <span className="text-[8px] text-gray-500 font-bold uppercase tracking-wider ml-1">Hasta</span>
                                <input
                                    type="date"
                                    value={customRange.end ? customRange.end.toISOString().split('T')[0] : ''}
                                    onChange={(e) => setCustomRange({ ...customRange, end: e.target.value ? new Date(e.target.value) : null })}
                                    className="bg-[#1A1A1A] border border-white/10 rounded-lg px-2 py-1 text-[10px] text-white focus:outline-none focus:border-gamer-green"
                                />
                            </div>
                        </div>
                    )}
                </div>

                <MediaKit
                    isOpen={showMediaKit}
                    onClose={() => setShowMediaKit(false)}
                    totalSubscribers={channelStats ? channelStats.subscribers : (stats.current.subscribers || 0)}
                    videos={videos}
                    channelName={channelStats?.title}
                />

                {error && (
                    <div className="mb-8 p-6 bg-red-900/20 border border-red-500/50 rounded-3xl flex items-center gap-6 animate-in slide-in-from-top">
                        <div className="bg-red-500 p-3 rounded-2xl text-black">
                            <Activity size={24} />
                        </div>
                        <div className="flex-1">
                            <p className="text-red-500 font-black text-xs uppercase tracking-[2px] mb-1 italic">Conexión Fallida</p>
                            <p className="text-base text-white font-bold">{error}</p>
                        </div>
                        <button onClick={() => window.location.reload()} className="px-6 py-3 bg-red-500 hover:bg-red-600 text-black font-black text-xs uppercase tracking-widest rounded-xl transition-all">Reintentar</button>
                    </div>
                )}

                <main className="animate-in fade-in duration-700">
                    {/* --- KPI Grid --- */}
                    <section className="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-5 mb-10">
                        <KpiCard icon={<Play size={18} />} label="Videos Totales" value={videos.length} loading={loading} />
                        <KpiCard icon={<TrendingUp size={18} />} label="Vistas (Periodo)" value={stats.current.views.toLocaleString()} diff={timeframe === 'all' ? undefined : stats.diffs.views} loading={loading} highlight />
                        <KpiCard
                            icon={<Users size={18} />}
                            label={timeframe === 'all' ? "Subs Totales" : "Nuevos Subs"}
                            value={timeframe === 'all' ? (channelStats?.subscribers ?? 0).toLocaleString() : stats.current.subscribers.toLocaleString()}
                            diff={timeframe === 'all' ? undefined : stats.diffs.subscribers}
                            loading={loading}
                        />
                        <KpiCard icon={<ThumbsUp size={18} />} label="Likes" value={stats.current.likes.toLocaleString()} diff={timeframe === 'all' ? undefined : stats.diffs.likes} loading={loading} />
                    </section>

                    {/* --- Content Area --- */}
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">

                        {/* Charts Section */}
                        {!expandContent && (
                            <div className="lg:col-span-2 space-y-8">
                                {/* Metric Switcher */}
                                <div className="flex gap-2 mb-4 overflow-x-auto no-scrollbar">
                                    {(['views', 'likes', 'comments', 'subscribers'] as const).map(m => (
                                        <button
                                            key={m}
                                            onClick={() => setActiveMetric(m)}
                                            className={`px-4 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all border ${activeMetric === m ? 'bg-gamer-green text-black border-gamer-green' : 'bg-transparent text-gray-500 border-gamer-border hover:border-gamer-green/50 hover:text-white'}`}
                                        >
                                            {m === 'views' ? 'Vistas' : m === 'likes' ? 'Likes' : m === 'comments' ? 'Coments' : 'Subs'}
                                        </button>
                                    ))}
                                </div>

                                <GrowthChart data={chartData} loading={loading} bestDay={bestDay} />

                                {/* Monthly Stats Table (Stacked below chart) */}
                                <MonthChart data={monthlyStats} />
                            </div>
                        )}

                        {/* Video List (Fixed Top 5) / Expanded Table */}
                        <VideoList
                            videos={expandContent ? videos : topVideos}
                            loading={loading}
                            expanded={expandContent}
                            onToggleExpand={() => setExpandContent(!expandContent)}
                        />
                    </div>
                </main>
            </div>
        </div>
    )
}
