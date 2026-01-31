import { Calendar } from 'lucide-react';

interface MonthlyStat {
    month: string;
    views: number;
    likes: number;
    comments: number;
}

interface MonthTableProps {
    data: MonthlyStat[];
}

export function MonthTable({ data }: MonthTableProps) {
    return (
        <div className="bg-gamer-card border border-gamer-border rounded-3xl p-6 md:p-8 shadow-xl shadow-black/60 w-full">
            <div className="flex items-center gap-3 mb-8">
                <Calendar className="text-gamer-green w-6 h-6" />
                <h3 className="text-xl font-black italic">📅 TOP MESES HISTÓRICOS</h3>
            </div>

            <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="border-b border-gamer-border text-gray-500 text-[10px] uppercase tracking-widest">
                            <th className="p-4">Mes</th>
                            <th className="p-4 text-right">Vistas</th>
                            <th className="p-4 text-right">Likes</th>
                            <th className="p-4 text-right">Comentarios</th>
                            <th className="p-4 text-right">Engagement</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {data.map((m) => {
                            const engagement = ((m.likes + m.comments) / m.views * 100).toFixed(2);
                            // Parse YYYY-MM to readable date
                            const [year, month] = m.month.split('-');
                            const date = new Date(parseInt(year), parseInt(month) - 1);
                            const monthName = date.toLocaleDateString('es-ES', { month: 'long', year: 'numeric' });

                            return (
                                <tr key={m.month} className="border-b border-gamer-border/50 hover:bg-white/5 transition-colors group">
                                    <td className="p-4 font-black capitalize text-white group-hover:text-gamer-green transition-colors">{monthName}</td>
                                    <td className="p-4 text-right font-mono text-gray-300">{m.views.toLocaleString()}</td>
                                    <td className="p-4 text-right font-mono text-gray-400">{m.likes.toLocaleString()}</td>
                                    <td className="p-4 text-right font-mono text-gray-400">{m.comments.toLocaleString()}</td>
                                    <td className="p-4 text-right font-bold text-gamer-green">{engagement}%</td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
