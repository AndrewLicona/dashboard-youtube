import { useState, useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { Calendar } from 'lucide-react';

interface MonthlyStat {
    month: string;
    views: number;
    likes: number;
    comments: number;
    subscribers: number;
}

interface MonthChartProps {
    data: MonthlyStat[]; // Expects full monthly data
}

export function MonthChart({ data }: MonthChartProps) {
    const [activeMetric, setActiveMetric] = useState<'views' | 'likes' | 'comments' | 'subscribers'>('views');

    // Sort data top to bottom based on active metric logic
    const chartData = useMemo(() => {
        // Create a copy and sort by active metric descending
        const sorted = [...data].sort((a, b) => b[activeMetric] - a[activeMetric]).slice(0, 12);

        return sorted.map(d => {
            const [year, month] = d.month.split('-');
            const date = new Date(parseInt(year), parseInt(month) - 1);
            return {
                name: date.toLocaleDateString('es-ES', { month: 'short', year: '2-digit' }),
                value: d[activeMetric],
                fullDate: date.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' }),
                original: d
            };
        });
    }, [data, activeMetric]);

    // Cleanup: Total value logic is unused for display now, can keep or remove. Kept for safety.

    return (
        <div className="bg-gamer-card border border-gamer-border rounded-3xl p-6 md:p-8 shadow-xl shadow-black/60 w-full relative group">
            <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-4">
                <div className="flex flex-col md:flex-row items-center gap-3 text-center md:text-left">
                    <Calendar className="text-gamer-green w-6 h-6 mb-1 md:mb-0" />
                    <div>
                        <h3 className="text-xl font-black italic uppercase">
                            Top Meses: <span className="text-white/80">{activeMetric === 'views' ? 'Vistas' : activeMetric === 'likes' ? 'Likes' : activeMetric === 'comments' ? 'Coments' : 'Subs'}</span>
                        </h3>
                        <p className="text-[10px] text-gray-500 font-bold tracking-widest uppercase">Ordenado por rendimiento</p>
                    </div>
                </div>

                {/* Metric Switcher - Dynamic: Hides active metric */}
                <div className="w-full md:w-auto flex justify-center gap-2 overflow-x-auto no-scrollbar bg-black/20 p-1.5 rounded-xl border border-white/5 pr-4">
                    {(['views', 'likes', 'comments', 'subscribers'] as const).map(m => {
                        if (activeMetric === m) return null; // Hide active button
                        return (
                            <button
                                key={m}
                                onClick={() => setActiveMetric(m)}
                                className={`flex-shrink-0 px-4 py-2 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all text-gray-500 hover:text-white hover:bg-white/5`}
                            >
                                {m === 'views' ? 'Vistas' : m === 'likes' ? 'Likes' : m === 'comments' ? 'Coments' : 'Subs'}
                            </button>
                        );
                    })}
                </div>
            </div>

            <div className="h-[350px] w-full relative">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                        <CartesianGrid strokeDasharray="3 3" horizontal={true} vertical={false} stroke="#262626" />
                        <XAxis type="number" stroke="#666" fontSize={10} tickLine={false} axisLine={false} tickFormatter={(v) => v >= 1000 ? `${(v / 1000).toFixed(0)}k` : v} />
                        <YAxis dataKey="name" type="category" stroke="#fff" fontSize={11} fontWeight="bold" width={60} tickLine={false} axisLine={false} />
                        <Tooltip
                            cursor={{ fill: '#ffffff05' }}
                            content={({ active, payload }) => {
                                if (active && payload && payload.length) {
                                    const data = payload[0].payload;
                                    return (
                                        <div className="bg-[#1A1A1A] border border-gamer-border p-3 rounded-xl shadow-xl">
                                            <p className="text-gamer-green font-black text-xs uppercase mb-1">{data.fullDate}</p>
                                            <p className="text-white font-bold text-lg">
                                                {data.value.toLocaleString()}
                                                <span className="text-[10px] text-gray-500 ml-1 uppercase">
                                                    {activeMetric === 'subscribers' ? 'Subs' : activeMetric === 'views' ? 'Vistas' : activeMetric}
                                                </span>
                                            </p>
                                        </div>
                                    );
                                }
                                return null;
                            }}
                        />
                        <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={20} animationDuration={1000}>
                            {chartData.map((_, index) => (
                                <Cell key={`cell-${index}`} fill={index === 0 ? '#00C851' : '#00C85180'} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
