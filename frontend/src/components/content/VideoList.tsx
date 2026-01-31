import { useState, useMemo } from 'react';
import { Play, TrendingUp, ThumbsUp, ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react';
import type { Video } from '../../types';

interface VideoListProps {
    videos: Video[];
    loading: boolean;
    expanded: boolean;
    onToggleExpand: () => void;
}

type SortKey = 'Vistas' | 'Likes' | 'Comentarios' | 'Publicado' | 'Engagement';

export function VideoList({ videos, loading, expanded, onToggleExpand }: VideoListProps) {
    const [sortConfig, setSortConfig] = useState<{ key: SortKey; direction: 'asc' | 'desc' }>({
        key: 'Vistas',
        direction: 'desc'
    });

    const handleSort = (key: SortKey) => {
        setSortConfig(current => ({
            key,
            direction: current.key === key && current.direction === 'desc' ? 'asc' : 'desc'
        }));
    };

    const sortedVideos = useMemo(() => {
        if (!expanded) return videos; // No sorting needed for sidebar view (always fixed top 5)

        return [...videos].sort((a, b) => {
            let aValue: number | string = 0;
            let bValue: number | string = 0;

            if (sortConfig.key === 'Engagement') {
                aValue = (a.Likes + a.Comentarios) / a.Vistas;
                bValue = (b.Likes + b.Comentarios) / b.Vistas;
            } else if (sortConfig.key === 'Publicado') {
                aValue = new Date(a.Publicado).getTime();
                bValue = new Date(b.Publicado).getTime();
            } else {
                aValue = a[sortConfig.key];
                bValue = b[sortConfig.key];
            }

            if (aValue < bValue) return sortConfig.direction === 'asc' ? -1 : 1;
            if (aValue > bValue) return sortConfig.direction === 'asc' ? 1 : -1;
            return 0;
        });
    }, [videos, expanded, sortConfig]);

    const SortIcon = ({ column }: { column: SortKey }) => {
        if (sortConfig.key !== column) return <ArrowUpDown size={12} className="opacity-30" />;
        return sortConfig.direction === 'asc' ? <ArrowUp size={12} className="text-gamer-green" /> : <ArrowDown size={12} className="text-gamer-green" />;
    };

    if (expanded) {
        return (
            <div className="bg-gamer-card border border-gamer-border rounded-3xl p-6 md:p-8 shadow-xl shadow-black/60 animate-in fade-in zoom-in-95 duration-300 col-span-1 lg:col-span-3">
                <div className="flex justify-between items-start md:items-center mb-6 md:mb-8 flex-col md:flex-row gap-4 md:gap-0">
                    <div>
                        <h3 className="text-xl font-black italic uppercase">
                            BIBLIOTECA <span className="md:hidden">: <span className="text-white/80">{sortConfig.key}</span></span> <span className="hidden md:inline">DE CONTENIDO</span>
                        </h3>
                        <p className="md:hidden text-[10px] text-gray-500 font-bold tracking-widest uppercase mt-1">Ordenado por {sortConfig.key}</p>
                    </div>

                    {/* --- MOBILE SORTING (Dynamic: Hides active) --- */}
                    <div className="md:hidden w-full overflow-x-auto no-scrollbar flex gap-2 pb-2">
                        {(['Publicado', 'Vistas', 'Likes', 'Engagement'] as SortKey[]).map((key) => {
                            if (sortConfig.key === key) return null; // Hide active button
                            return (
                                <button
                                    key={key}
                                    onClick={() => handleSort(key)}
                                    className="px-4 py-2 rounded-lg text-[10px] font-bold uppercase tracking-wider whitespace-nowrap transition-all border border-white/10 bg-white/5 text-gray-400 hover:bg-white/10"
                                >
                                    {key}
                                </button>
                            );
                        })}
                    </div>

                    <button onClick={onToggleExpand} className="hidden md:block text-xs text-gamer-green font-bold uppercase hover:underline">
                        Volver a Top 5
                    </button>
                </div>

                <div className="border border-gamer-border rounded-xl bg-[#0F0F0F] overflow-hidden">
                    <div className="max-h-[80vh] lg:max-h-[calc(100vh-200px)] overflow-y-auto no-scrollbar">

                        {/* --- MOBILE CARD VIEW --- */}
                        <div className="md:hidden flex flex-col divide-y divide-white/5">
                            {sortedVideos.map((v) => {
                                const engagement = ((v.Likes + v.Comentarios) / v.Vistas * 100).toFixed(2);
                                return (
                                    <div key={v["Video ID"]} className="p-4 flex gap-4">
                                        {/* Thumbnail specific for mobile card */}
                                        <div className="relative min-w-[120px] w-[120px] h-[68px]">
                                            <img src={v.Miniatura} alt="" className="w-full h-full object-cover rounded-lg" />
                                            <div className="absolute bottom-1 right-1 bg-black/80 px-1.5 py-0.5 rounded text-[8px] font-bold text-white">
                                                {new Date(v.Publicado).toLocaleDateString()}
                                            </div>
                                        </div>

                                        <div className="flex-1 min-w-0 flex flex-col justify-between">
                                            <h4 className="text-xs font-bold text-white line-clamp-2 leading-snug mb-2">{v.Titulo}</h4>

                                            <div className="grid grid-cols-2 gap-x-4 gap-y-1">
                                                <div className="flex items-center gap-1.5 text-[10px] text-gray-400">
                                                    <Play size={10} className="text-gamer-green" />
                                                    <span className="font-bold text-white">{v.Vistas.toLocaleString()}</span>
                                                </div>
                                                <div className="flex items-center gap-1.5 text-[10px] text-gray-400">
                                                    <ThumbsUp size={10} className="text-white" />
                                                    <span>{v.Likes.toLocaleString()}</span>
                                                </div>
                                                <div className="flex items-center gap-1.5 text-[10px] text-gray-400">
                                                    <TrendingUp size={10} className="text-gamer-green" />
                                                    <span className="text-gamer-green font-bold">{engagement}%</span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>

                        {/* --- DESKTOP TABLE VIEW --- */}
                        <table className="w-full text-left border-collapse relative hidden md:table">
                            <thead className="sticky top-0 bg-[#0F0F0F] z-10 shadow-lg shadow-black/20">
                                <tr className="border-b border-gamer-border text-gray-500 text-[10px] uppercase tracking-widest">
                                    <th className="p-4 bg-[#0F0F0F]">Video</th>

                                    <th className="p-4 text-right bg-[#0F0F0F] cursor-pointer hover:bg-white/5 transition-colors hidden md:table-cell" onClick={() => handleSort('Publicado')}>
                                        <div className="flex items-center justify-end gap-2">
                                            Publicado <SortIcon column="Publicado" />
                                        </div>
                                    </th>

                                    <th className="p-4 text-right bg-[#0F0F0F] cursor-pointer hover:bg-white/5 transition-colors" onClick={() => handleSort('Vistas')}>
                                        <div className="flex items-center justify-end gap-2">
                                            Vistas <SortIcon column="Vistas" />
                                        </div>
                                    </th>

                                    <th className="p-4 text-right bg-[#0F0F0F] cursor-pointer hover:bg-white/5 transition-colors" onClick={() => handleSort('Likes')}>
                                        <div className="flex items-center justify-end gap-2">
                                            Likes <SortIcon column="Likes" />
                                        </div>
                                    </th>

                                    <th className="p-4 text-right bg-[#0F0F0F] cursor-pointer hover:bg-white/5 transition-colors hidden lg:table-cell" onClick={() => handleSort('Comentarios')}>
                                        <div className="flex items-center justify-end gap-2">
                                            Comentarios <SortIcon column="Comentarios" />
                                        </div>
                                    </th>

                                    <th className="p-4 text-right bg-[#0F0F0F] cursor-pointer hover:bg-white/5 transition-colors hidden md:table-cell" onClick={() => handleSort('Engagement')}>
                                        <div className="flex items-center justify-end gap-2">
                                            Engagement <SortIcon column="Engagement" />
                                        </div>
                                    </th>
                                </tr>
                            </thead>
                            <tbody className="text-sm">
                                {sortedVideos.map((v) => {
                                    const engagement = ((v.Likes + v.Comentarios) / v.Vistas * 100).toFixed(2);
                                    return (
                                        <tr key={v["Video ID"]} className="border-b border-gamer-border/50 hover:bg-white/5 transition-colors">
                                            <td className="p-4 min-w-[200px] md:min-w-[300px]">
                                                <div className="flex gap-4 items-center">
                                                    <img src={v.Miniatura} alt="" className="w-16 h-9 object-cover rounded-lg" />
                                                    <span className="font-bold line-clamp-2 text-xs md:text-sm">{v.Titulo}</span>
                                                </div>
                                            </td>
                                            <td className="p-4 text-right font-mono text-gray-400 hidden md:table-cell">{new Date(v.Publicado).toLocaleDateString()}</td>
                                            <td className="p-4 text-right font-black">{v.Vistas.toLocaleString()}</td>
                                            <td className="p-4 text-right text-gray-300">{v.Likes.toLocaleString()}</td>
                                            <td className="p-4 text-right text-gray-300 hidden lg:table-cell">{v.Comentarios.toLocaleString()}</td>
                                            <td className="p-4 text-right text-gamer-green font-bold hidden md:table-cell">{engagement}%</td>
                                        </tr>
                                    )
                                })}
                            </tbody>
                        </table>
                    </div>
                </div>

            </div>
        )
    }

    // Sidebar View
    return (
        <aside className="bg-gamer-card border border-gamer-border rounded-3xl p-6 md:p-8 shadow-xl shadow-black/60 sticky top-8">
            <div className="flex items-center justify-between mb-8">
                <h3 className="text-xl font-black italic">🏆 TOP CONTENIDO</h3>
                <span className="text-[10px] bg-white/5 border border-white/10 px-2 py-1 rounded text-gray-400 font-bold">POR VISTAS</span>
            </div>
            <div className="space-y-6">
                {videos.slice(0, 5).map((v) => (
                    <div key={v["Video ID"]} className="flex gap-4 items-center group cursor-pointer">
                        <div className="relative min-w-[100px] w-[100px] h-[60px] rounded-xl overflow-hidden border border-gamer-border group-hover:border-gamer-green transition-all">
                            <img src={v.Miniatura} alt="" className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                            <div className="absolute inset-0 bg-black/40" />
                            <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                                <Play size={20} className="fill-gamer-green text-gamer-green" />
                            </div>
                        </div>
                        <div className="flex-1 overflow-hidden">
                            <h4 className="text-[13px] font-black line-clamp-2 leading-tight mb-1 group-hover:text-gamer-green transition-colors">{v.Titulo}</h4>
                            <div className="flex items-center gap-1.5 text-gray-500">
                                <TrendingUp size={10} className="text-gamer-green/60" />
                                <span className="text-[10px] font-black italic">{v.Vistas.toLocaleString()}</span>
                                <span className="text-[10px] text-gray-600">•</span>
                                <ThumbsUp size={10} className="text-gray-600" />
                                <span className="text-[10px] text-gray-500">{v.Likes.toLocaleString()}</span>
                            </div>
                        </div>
                    </div>
                ))}

                {loading && [1, 2, 3, 4, 5].map(i => (
                    <div key={i} className="animate-pulse flex gap-4 items-center">
                        <div className="min-w-[100px] h-[60px] bg-white/5 rounded-xl" />
                        <div className="flex-1 space-y-2">
                            <div className="h-3 w-full bg-white/5 rounded" />
                            <div className="h-2 w-1/2 bg-white/5 rounded" />
                        </div>
                    </div>
                ))}
            </div>

            <button onClick={onToggleExpand} className="w-full mt-10 py-4 bg-gamer-green/5 hover:bg-gamer-green/10 border border-gamer-green/20 hover:border-gamer-green/40 text-gamer-green text-[10px] font-black uppercase tracking-[3px] rounded-2xl transition-all">
                Ver Todo el Contenido
            </button>
        </aside>
    );
}
