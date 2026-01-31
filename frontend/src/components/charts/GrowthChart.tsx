import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, Calendar } from 'lucide-react';

interface GrowthChartProps {
    data: { name: string; value: number; date: string }[];
    loading: boolean;
    bestDay?: { date: string; value: number; metric: string };
}

export function GrowthChart({ data, loading, bestDay }: GrowthChartProps) {
    return (
        <div className="bg-gamer-card border border-gamer-border rounded-3xl p-6 md:p-8 shadow-xl shadow-black/60 relative overflow-hidden group">
            <div className="absolute top-0 right-0 w-32 h-32 bg-gamer-green/5 blur-3xl -mr-16 -mt-16 pointer-events-none" />

            <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-8 gap-4">
                <div className="flex flex-col md:flex-row md:items-baseline md:gap-4">
                    <h3 className="text-xl font-black flex items-center gap-3">
                        <TrendingUp className="text-gamer-green w-6 h-6" />
                        Rendimiento del Canal
                    </h3>
                    <span className="text-[10px] font-black uppercase text-gray-500 tracking-widest ml-9 md:ml-0">métricas diarias</span>
                </div>

                {bestDay && !loading && (
                    <div className="bg-gamer-green/10 border border-gamer-green/20 px-4 py-2 rounded-xl flex items-center gap-3 self-start md:self-auto">
                        <span className="text-[9px] font-black text-gamer-green uppercase tracking-widest flex items-center gap-1.5 shrink-0">
                            <Calendar size={12} /> Mejor Día
                        </span>

                        <div className="w-px h-4 bg-gamer-green/20"></div>

                        <div className="flex items-baseline gap-2">
                            <span className="text-white font-black text-sm whitespace-nowrap">
                                {new Date(bestDay.date).toLocaleDateString(undefined, { day: 'numeric', month: 'short' })}
                            </span>
                            <span className="text-gray-400 text-[10px] font-bold whitespace-nowrap">
                                {bestDay.value.toLocaleString()} {bestDay.metric === 'views' ? 'vistas' : bestDay.metric}
                            </span>
                        </div>
                    </div>
                )}
            </div>

            <div className="h-[350px] w-full">
                {loading ? (
                    <div className="w-full h-full bg-black/20 rounded-2xl animate-pulse border border-dashed border-gamer-border flex items-center justify-center">
                        <span className="text-gray-600 font-bold uppercase tracking-widest text-xs">Cargando datos...</span>
                    </div>
                ) : (
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={data}>
                            <defs>
                                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#00C851" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="#00C851" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#262626" />
                            <XAxis dataKey="name" stroke="#666" fontSize={10} tickLine={false} axisLine={false} dy={10} minTickGap={30} />
                            <YAxis stroke="#666" fontSize={10} tickLine={false} axisLine={false} tickFormatter={(v) => v >= 1000 ? `${(v / 1000).toFixed(1)}k` : v} />
                            <Tooltip
                                contentStyle={{ backgroundColor: '#1A1A1A', border: '1px solid #262626', borderRadius: '12px', color: '#fff' }}
                                cursor={{ stroke: '#00C851', strokeWidth: 2 }}
                            />
                            <Area type="monotone" dataKey="value" stroke="#00C851" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" animationDuration={1500} />
                        </AreaChart>
                    </ResponsiveContainer>
                )}
            </div>

        </div>
    );
}
