import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Play } from 'lucide-react';

export function LandingPage() {
    const navigate = useNavigate();

    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        if (params.get('auth_success') === 'true' && params.get('channel_id')) {
            const channelId = params.get('channel_id')!;

            // Save as legitimate "logged in" user
            localStorage.setItem('yt_channel_id', channelId);

            // Redirect to their personal dashboard
            navigate(`/dashboard/${channelId}`);
        }
    }, [navigate]);

    return (
        <div className="min-h-screen bg-[#0F0F0F] text-white font-sans flex flex-col items-center justify-center p-4">
            <div className="max-w-2xl text-center space-y-8 animate-in fade-in zoom-in duration-500">

                {/* Logo / Icon */}
                <div className="inline-flex p-6 bg-gamer-green/10 rounded-3xl border border-gamer-green/20 mb-4 shadow-[0_0_50px_rgba(0,255,0,0.1)]">
                    <Play size={64} className="text-gamer-green fill-gamer-green" />
                </div>

                <h1 className="text-5xl md:text-7xl font-black tracking-tighter uppercase italic">
                    Tu Canal <br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-gamer-green to-emerald-600">
                        Next Level
                    </span>
                </h1>

                <p className="text-gray-400 text-lg md:text-xl font-medium max-w-lg mx-auto leading-relaxed">
                    Muestra tus métricas de manera fácil y profesional a <span className="text-white font-bold">posibles patrocinadores e interesados</span>. Datos verificados en tiempo real, sin capturas de pantalla.
                </p>

                <div className="pt-8">
                    <a
                        href="/api/auth/login"
                        className="group relative inline-flex items-center gap-4 px-8 py-4 bg-gamer-green text-black font-black text-lg uppercase tracking-widest rounded-2xl hover:bg-emerald-400 transition-all hover:scale-105 active:scale-95"
                    >
                        <span className="relative z-10">Conectar con YouTube</span>
                        <div className="absolute inset-0 bg-white/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity" />
                    </a>

                    <p className="mt-4 text-xs text-gray-600 font-bold uppercase tracking-widest">
                        100% Seguro • Solo Lectura • Sin Suscripción
                    </p>
                </div>
            </div>
        </div>
    );
}
