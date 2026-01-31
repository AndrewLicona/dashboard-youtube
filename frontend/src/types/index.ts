export interface Video {
    "Video ID": string;
    Titulo: string;
    Publicado: string;
    Miniatura: string;
    Vistas: number;
    Likes: number;
    Comentarios: number;
}

export interface DailyStat {
    day: string;
    views: number;
    likes: number;
    comments: number;
    subscribers: number;
}

export type Timeframe = '7d' | '15d' | '30d' | 'all' | 'custom';

export interface DateRange {
    start: Date | null;
    end: Date | null;
}
