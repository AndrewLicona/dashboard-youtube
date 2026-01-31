import { X, Download, Star, Users, Eye, MousePointerClick } from 'lucide-react';
import type { Video } from '../../types';

interface MediaKitProps {
    isOpen: boolean;
    onClose: () => void;
    totalSubscribers: number;
    videos: Video[];
    channelName?: string;
}

export function MediaKit({ isOpen, onClose, totalSubscribers, videos, channelName = "AJDREW" }: MediaKitProps) {
    if (!isOpen) return null;

    // --- Calculations ---
    const last10Videos = videos.slice(0, 10);
    const avgViews = last10Videos.reduce((acc, v) => acc + v.Vistas, 0) / (last10Videos.length || 1);

    // Engagement Rate = (Total Interactions / Total Views) * 100
    // Using last 10 videos for a more current representation
    const totalInteractions = last10Videos.reduce((acc, v) => acc + v.Likes + v.Comentarios, 0);
    const totalViewsLast10 = last10Videos.reduce((acc, v) => acc + v.Vistas, 0);
    const engagementRate = totalViewsLast10 > 0 ? (totalInteractions / totalViewsLast10) * 100 : 0;

    const consistencyScore = "Alta"; // Placeholder logic: could be based on publish frequency

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-300">
            {/* Modal Container (Printable Area) */}
            <div className="bg-white text-black w-full max-w-4xl max-h-[90vh] overflow-y-auto rounded-3xl shadow-2xl relative">

                {/* Header Actions (Not Printed) */}
                <div className="sticky top-0 right-0 p-4 flex justify-end gap-2 bg-white/90 backdrop-blur print:hidden z-10">
                    <button onClick={() => window.print()} className="flex items-center gap-2 px-4 py-2 bg-black text-white rounded-full font-bold hover:bg-gray-800 transition-colors">
                        <Download size={18} />
                        <span className="text-xs uppercase tracking-widest">Imprimir / PDF</span>
                    </button>
                    <button onClick={onClose} className="p-2 bg-gray-100 rounded-full hover:bg-gray-200 transition-colors">
                        <X size={18} />
                    </button>
                </div>

                <div className="p-8 md:p-12 print:p-0">
                    {/* --- HEADER IDENTITY --- */}
                    <header className="flex flex-col md:flex-row justify-between items-start md:items-center border-b-4 border-black pb-8 mb-8">
                        <div>
                            <h1 className="text-5xl md:text-6xl font-black uppercase tracking-tighter mb-2">{channelName}</h1>
                            <p className="text-xl font-bold text-gray-500 uppercase tracking-widest">Media Kit & Sponsorships</p>
                        </div>
                        <div className="mt-6 md:mt-0 text-right">
                            <div className="bg-black text-white px-6 py-2 rounded-full inline-block mb-2">
                                <span className="font-black uppercase tracking-widest text-xs">Gaming & Tech Creator</span>
                            </div>
                            <p className="text-sm font-medium text-gray-500">contact@ajdrew.com</p>
                        </div>
                    </header>

                    {/* --- HERO METRICS --- */}
                    <section className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
                        <div className="bg-gray-50 p-6 rounded-2xl border-2 border-dashed border-gray-200 text-center">
                            <Users className="w-8 h-8 mx-auto mb-2 text-black" />
                            <h3 className="text-4xl font-black mb-1">{totalSubscribers.toLocaleString()}</h3>
                            <p className="text-xs font-bold uppercase tracking-widest text-gray-400">Suscriptores Totales</p>
                        </div>
                        <div className="bg-gray-50 p-6 rounded-2xl border-2 border-dashed border-gray-200 text-center">
                            <Eye className="w-8 h-8 mx-auto mb-2 text-black" />
                            <h3 className="text-4xl font-black mb-1">{Math.round(avgViews).toLocaleString()}</h3>
                            <p className="text-xs font-bold uppercase tracking-widest text-gray-400">Promedio Vistas (Ult. 10)</p>
                        </div>
                        <div className="bg-black text-white p-6 rounded-2xl border-2 border-black text-center shadow-[8px_8px_0px_0px_rgba(0,0,0,0.2)]">
                            <MousePointerClick className="w-8 h-8 mx-auto mb-2 text-gamer-green" />
                            <h3 className="text-4xl font-black mb-1 text-gamer-green">{engagementRate.toFixed(1)}%</h3>
                            <p className="text-xs font-bold uppercase tracking-widest text-gray-400">Engagement Rate</p>
                        </div>
                    </section>

                    {/* --- DEMOGRAPHICS & CONTENT --- */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-12 mb-12">
                        <div>
                            <h4 className="text-2xl font-black uppercase mb-6 flex items-center gap-2">
                                <Star className="fill-black" size={20} />
                                Top Contenido Exitoso
                            </h4>
                            <div className="space-y-4">
                                {last10Videos.slice(0, 3).map((v, i) => (
                                    <div key={i} className="flex gap-4 items-center border-b border-gray-100 pb-4">
                                        <div className="font-black text-3xl text-gray-200">0{i + 1}</div>
                                        <div>
                                            <p className="font-bold text-sm line-clamp-1">{v.Titulo}</p>
                                            <p className="text-xs text-gray-500 font-mono mt-1">
                                                {v.Vistas.toLocaleString()} Vistas • {((v.Likes + v.Comentarios) / v.Vistas * 100).toFixed(1)}% Eng.
                                            </p>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div>
                            <h4 className="text-2xl font-black uppercase mb-6">Por qué colaborar</h4>
                            <p className="text-gray-600 leading-relaxed mb-6 font-medium">
                                Una audiencia altamente comprometida, enfocada en gaming y tecnología.
                                Contenido consistente con una tasa de retención superior al promedio del mercado.
                                Estilo visual único y profesional que garantiza la mejor presentación para tu marca.
                            </p>

                            <div className="grid grid-cols-2 gap-4">
                                <div className="bg-gray-100 p-4 rounded-xl">
                                    <span className="block text-2xl font-black">Daily</span>
                                    <span className="text-[10px] uppercase font-bold text-gray-500">Frecuencia de Videos</span>
                                </div>
                                <div className="bg-gray-100 p-4 rounded-xl">
                                    <span className="block text-2xl font-black">{consistencyScore}</span>
                                    <span className="text-[10px] uppercase font-bold text-gray-500">Consistencia</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* --- FOOTER --- */}
                    <footer className="text-center border-t-2 border-gray-100 pt-8">
                        <p className="font-black text-xl uppercase tracking-tighter">Ready to Level Up?</p>
                        <p className="text-gray-400 text-sm">Generated by AjDrew Analytics Suite</p>
                    </footer>

                </div>
            </div>
        </div>
    );
}
