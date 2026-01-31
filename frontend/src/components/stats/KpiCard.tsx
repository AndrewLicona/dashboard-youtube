import type { ReactNode } from 'react';

interface KpiCardProps {
    icon: ReactNode;
    label: string;
    value: string | number;
    diff?: number;
    loading: boolean;
    highlight?: boolean;
}

export function KpiCard({ icon, label, value, diff, loading, highlight }: KpiCardProps) {
    const isPositive = diff !== undefined && diff > 0;

    return (
        <div className={`bg-gamer-card border ${highlight ? 'border-gamer-green/30 relative overflow-hidden' : 'border-gamer-border'} p-4 md:p-6 rounded-3xl shadow-lg hover:translate-y-[-4px] transition-all group`}>
            {highlight && <div className="absolute top-0 right-0 w-24 h-24 bg-gamer-green/10 blur-2xl -mr-12 -mt-12" />}

            <div className="flex justify-between items-start mb-3 md:mb-5 h-8">
                <div className={`p-2 md:p-2.5 rounded-xl ${highlight ? 'bg-gamer-green text-black' : 'bg-black/40 text-gray-400 group-hover:text-gamer-green transition-colors'}`}>
                    {icon}
                </div>
                {diff !== undefined && !loading && !isNaN(diff) && (
                    <div className={`flex items-center gap-1 px-1.5 py-1 rounded-lg text-[9px] md:text-[10px] font-black ${isPositive ? 'bg-gamer-green/10 text-gamer-green' : 'bg-red-500/10 text-red-500'}`}>
                        {isPositive ? '↑' : '↓'} {Math.abs(diff).toFixed(1)}%
                    </div>
                )}
            </div>

            {loading ? (
                <div className="h-6 md:h-9 w-20 md:w-32 bg-white/5 animate-pulse rounded-lg" />
            ) : (
                <p className={`text-lg md:text-3xl font-black ${highlight ? 'text-gamer-green' : 'text-white'} tracking-tighter truncate`}>{value}</p>
            )}
            <p className="text-gray-500 text-[10px] font-black uppercase tracking-widest mt-1 md:mt-2 italic truncate">{label}</p>
        </div>
    );
}
