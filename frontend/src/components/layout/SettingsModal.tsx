import { useState, useEffect } from 'react';
import { X, Save, Key, Youtube } from 'lucide-react';

interface SettingsModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export function SettingsModal({ isOpen, onClose }: SettingsModalProps) {
    const [channelId, setChannelId] = useState('');
    const [apiKey, setApiKey] = useState('');

    useEffect(() => {
        if (isOpen) {
            setChannelId(localStorage.getItem('yt_channel_id') || '');
            setApiKey(localStorage.getItem('yt_api_key') || '');
        }
    }, [isOpen]);

    const handleSave = () => {
        if (channelId) localStorage.setItem('yt_channel_id', channelId);
        else localStorage.removeItem('yt_channel_id');

        if (apiKey) localStorage.setItem('yt_api_key', apiKey);
        else localStorage.removeItem('yt_api_key');

        onClose();
        window.location.reload(); // Simple reload to refresh all hooks
    };

    const handleClear = () => {
        localStorage.removeItem('yt_channel_id');
        localStorage.removeItem('yt_api_key');
        setChannelId('');
        setApiKey('');
        onClose();
        window.location.reload();
    };

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm animate-in fade-in">
            <div className="bg-[#1A1A1A] border border-gamer-border rounded-3xl w-full max-w-md p-6 shadow-2xl relative">
                <button onClick={onClose} className="absolute top-4 right-4 text-gray-500 hover:text-white transition-colors">
                    <X size={20} />
                </button>

                <div className="flex items-center gap-3 mb-6">
                    <div className="p-3 bg-gamer-green/10 rounded-xl text-gamer-green">
                        <Key size={24} />
                    </div>
                    <div>
                        <h2 className="text-xl font-black text-white uppercase italic">Configurar Canal</h2>
                        <p className="text-xs text-gray-400">Introduce tus credenciales de YouTube</p>
                    </div>
                </div>

                <div className="space-y-4">
                    <div>
                        <label className="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-2 flex items-center gap-2">
                            <Youtube size={12} /> Channel ID
                        </label>
                        <input
                            type="text"
                            value={channelId}
                            onChange={(e) => setChannelId(e.target.value)}
                            placeholder="Ej: UC1234567890..."
                            className="w-full bg-black/40 border border-gamer-border rounded-xl px-4 py-3 text-white focus:border-gamer-green focus:outline-none transition-colors text-sm font-mono"
                        />
                    </div>

                    <div>
                        <label className="block text-xs font-bold text-gray-400 uppercase tracking-widest mb-2 flex items-center gap-2">
                            <Key size={12} /> Google API Key
                        </label>
                        <input
                            type="password"
                            value={apiKey}
                            onChange={(e) => setApiKey(e.target.value)}
                            placeholder="AIzaSy..."
                            className="w-full bg-black/40 border border-gamer-border rounded-xl px-4 py-3 text-white focus:border-gamer-green focus:outline-none transition-colors text-sm font-mono"
                        />
                        <p className="text-[10px] text-gray-600 mt-2">
                            Tu API Key se guardará localmente en tu navegador. Necesaria para descargar datos de nuevos canales.
                        </p>
                        <a href="https://console.cloud.google.com/apis/credentials" target="_blank" rel="noreferrer" className="block mt-2 text-[10px] text-gamer-green hover:underline">
                            → Obtener API Key aquí
                        </a>
                    </div>
                </div>

                <div className="flex gap-3 mt-8">
                    <button
                        onClick={handleClear}
                        className="flex-1 py-3 bg-red-500/10 hover:bg-red-500/20 text-red-500 font-bold uppercase text-xs rounded-xl transition-all"
                    >
                        Resetear
                    </button>
                    <button
                        onClick={handleSave}
                        className="flex-1 py-3 bg-gamer-green hover:bg-gamer-green/90 text-black font-black uppercase text-xs rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg shadow-gamer-green/20"
                    >
                        <Save size={16} /> Guardar
                    </button>
                </div>
            </div>
        </div>
    );
}
