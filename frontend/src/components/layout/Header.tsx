import { useState } from 'react';
import { Activity, Verified, Settings, Briefcase } from 'lucide-react';
import { SettingsModal } from './SettingsModal';
//import type { Timeframe } from '../../types';


interface HeaderProps {
    onOpenMediaKit?: () => void;
    channelName?: string;
    channelAvatar?: string;
}

export function Header({ onOpenMediaKit, channelName, channelAvatar }: HeaderProps) {
    const [isSettingsOpen, setIsSettingsOpen] = useState(false);

    const displayName = channelName || "AJDREW";

    return (
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-6 border-b border-gamer-border pb-8">
            <div className="flex flex-col gap-1">
                <div className="flex items-center gap-3">
                    <div className="bg-gamer-green/10 p-2 rounded-xl overflow-hidden relative">
                        {channelAvatar ? (
                            <img src={channelAvatar} alt="Logo" className="w-8 h-8 object-cover rounded-full" />
                        ) : (
                            <Activity className="text-gamer-green w-8 h-8" />
                        )}
                    </div>
                    <h1 className="text-xl md:text-3xl font-black tracking-tighter uppercase break-words text-left">
                        {displayName} <span className="text-gamer-green block md:inline">Analytics</span>
                    </h1>
                </div>
                <div className="flex items-center gap-2 mt-1">
                    <span className="text-gray-400 font-bold ml-1">{displayName} Dashboard</span>
                    <Verified className="w-4 h-4 text-gamer-green fill-gamer-green/20" />
                </div>
            </div>

            <div className="flex items-center gap-6 self-end md:self-auto">
                <div className="flex items-center gap-2 bg-gamer-card p-1.5 rounded-2xl border border-gamer-border overflow-x-auto no-scrollbar">

                    <div className="flex items-center gap-4">
                        <button
                            onClick={() => window.open("/api/auth/login", "_blank")}
                            className="flex items-center gap-2 px-4 py-2 bg-[#1A1A1A] hover:bg-[#252525] border border-white/10 rounded-lg text-sm font-bold transition-all text-white"
                        >
                            <svg viewBox="0 0 24 24" className="w-4 h-4 fill-current"><path d="M12.545,10.539h-2.181c-0.27,0-0.485,0.222-0.489,0.492c-0.003,0.203-0.003,0.406,0,0.609 c0.004,0.27,0.219,0.492,0.489,0.492h2.181c1.239,0,2.247-1.008,2.247-2.247v-1.127c0-0.449-0.366-0.815-0.815-0.815h-0.27 c-0.449,0-0.815,0.366-0.815,0.815v0.582h-2.198l0.004-3.696l2.193-0.003v0.585c0,0.449,0.366,0.815,0.815,0.815h0.27 c0.449,0,0.815-0.366,0.815-0.815V5.099c0-1.239-1.008-2.247-2.247-2.247H6.938c-1.239,0-2.247,1.008-2.247,2.247v13.801 c0,1.239,1.008,2.247,2.247,2.247h5.607c1.239,0,2.247-1.008,2.247-2.247v-1.127c0-0.449-0.366-0.815-0.815-0.815h-0.27 c-0.449,0-0.815,0.366-0.815,0.815v0.582h-2.193l-0.004-3.696h2.198v0.585c0,0.449,0.366,0.815,0.815,0.815h0.27 c0.449,0,0.815-0.366,0.815-0.815v-1.637C14.792,11.547,13.784,10.539,12.545,10.539z M19.615,11.402l-2.673-2.731 c-0.315-0.321-0.852-0.098-0.852,0.354v1.731h-4.321c-0.276,0-0.5,0.224-0.5,0.5v1.488c0,0.276,0.224,0.5,0.5,0.5h4.321v1.731 c0,0.452,0.537,0.675,0.852,0.354l2.673-2.731C19.807,12.404,19.807,11.598,19.615,11.402z" /></svg>
                            Conectar Canal
                        </button>

                        {onOpenMediaKit && (
                            <button
                                onClick={onOpenMediaKit}
                                className="p-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-xl transition-colors"
                                title="Media Kit"
                            >
                                <Briefcase size={18} />
                            </button>
                        )}
                    </div>

                    <button
                        onClick={() => setIsSettingsOpen(true)}
                        className="p-2 text-gray-400 hover:text-white hover:bg-white/5 rounded-xl transition-colors"
                        title="Configurar API Keys"
                    >
                        <Settings size={18} />
                    </button>
                </div>

            </div>

            <SettingsModal isOpen={isSettingsOpen} onClose={() => setIsSettingsOpen(false)} />
        </header>
    );
}
