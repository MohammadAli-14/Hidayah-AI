# UI Implementation Rules
- Primary Framework: Streamlit.
- Branding: Use 'Hadayah AI.jpg' in the sidebar.
- Color Palette: Midnight Blue (#1a2a40), Emerald Green, Metallic Gold (#d4af37).
- Layout: Use a sidebar for Juz navigation and a main area with dual-pane text display (Arabic vs. Translation).
- Instruction: Inject the Tailwind-styled HTML from 'code.html' into the Streamlit app using st.markdown(unsafe_allow_html=True).

# Design Reference
<!DOCTYPE html>
<html class="dark" lang="en"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Hidayah AI Research Dashboard</title>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&amp;family=Inter:wght@300;400;500;600;700&amp;family=Playfair+Display:wght@600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,typography"></script>
<script>
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        primary: "#D4AF37", // Metallic Gold
                        "background-light": "#F8FAFC", // Slate 50
                        "background-dark": "#0F172A", // Deep Midnight Blue (darker than prompt for contrast)
                        "surface-dark": "#1A2A40", // Prompt Midnight Blue
                        "emerald-deep": "#064E3B",
                        "emerald-light": "#10B981",
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                        serif: ['Playfair Display', 'serif'],
                        arabic: ['Amiri', 'serif'],
                    },
                    borderRadius: {
                        DEFAULT: "0.75rem",
                    },
                    boxShadow: {
                        'glass': '0 4px 30px rgba(0, 0, 0, 0.1)',
                        'glow': '0 0 15px rgba(212, 175, 55, 0.2)',
                    }
                },
            },
        };
    </script>
<style>::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(212, 175, 55, 0.3);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(212, 175, 55, 0.5);
        }
        .glass-panel {
            background: rgba(26, 42, 64, 0.7);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .gold-gradient-text {
            background: linear-gradient(135deg, #D4AF37 0%, #F3E5AB 50%, #D4AF37 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
</head>
<body class="bg-background-light dark:bg-background-dark text-slate-800 dark:text-slate-100 font-sans h-screen overflow-hidden flex transition-colors duration-300">
<aside class="w-72 h-full glass-panel dark:glass-panel bg-white dark:bg-opacity-5 flex flex-col border-r border-slate-200 dark:border-slate-700/50 z-20 shadow-xl relative">
<div class="p-6 flex items-center space-x-3 border-b border-slate-200 dark:border-slate-700/30">
<div class="relative w-10 h-10 flex items-center justify-center rounded-full bg-gradient-to-br from-emerald-900 to-emerald-deep shadow-glow">
<span class="material-icons-round text-primary text-2xl">mosque</span>
<div class="absolute -top-1 -right-1 w-3 h-3 bg-primary rounded-full animate-pulse"></div>
</div>
<div>
<h1 class="text-xl font-serif font-bold text-slate-900 dark:text-white tracking-wide">Hidayah<span class="text-primary">AI</span></h1>
<p class="text-xs text-slate-500 dark:text-slate-400">Research Companion</p>
</div>
</div>
<div class="flex-1 overflow-y-auto p-4 space-y-2">
<h3 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 px-2">Juz Navigation</h3>
<button class="w-full flex items-center justify-between p-3 rounded-xl bg-primary/10 border border-primary/20 text-primary transition-all group">
<div class="flex items-center space-x-3">
<span class="flex items-center justify-center w-6 h-6 rounded-full bg-primary text-background-dark text-xs font-bold">1</span>
<span class="font-medium">Al-Fatiha &amp; Al-Baqarah</span>
</div>
<span class="material-icons-round text-sm group-hover:translate-x-1 transition-transform">chevron_right</span>
</button>
<button class="w-full flex items-center justify-between p-3 rounded-xl hover:bg-slate-100 dark:hover:bg-white/5 text-slate-600 dark:text-slate-300 transition-colors group">
<div class="flex items-center space-x-3">
<span class="flex items-center justify-center w-6 h-6 rounded-full border border-slate-300 dark:border-slate-600 text-xs text-slate-400">2</span>
<span class="font-medium">Sayaqulu</span>
</div>
</button>
<button class="w-full flex items-center justify-between p-3 rounded-xl hover:bg-slate-100 dark:hover:bg-white/5 text-slate-600 dark:text-slate-300 transition-colors group">
<div class="flex items-center space-x-3">
<span class="flex items-center justify-center w-6 h-6 rounded-full border border-slate-300 dark:border-slate-600 text-xs text-slate-400">3</span>
<span class="font-medium">Tilka ar-Rusul</span>
</div>
</button>
<button class="w-full flex items-center justify-between p-3 rounded-xl hover:bg-slate-100 dark:hover:bg-white/5 text-slate-600 dark:text-slate-300 transition-colors group">
<div class="flex items-center space-x-3">
<span class="flex items-center justify-center w-6 h-6 rounded-full border border-slate-300 dark:border-slate-600 text-xs text-slate-400">4</span>
<span class="font-medium">Lan Tanalu</span>
</div>
</button>
<button class="w-full flex items-center justify-between p-3 rounded-xl hover:bg-slate-100 dark:hover:bg-white/5 text-slate-600 dark:text-slate-300 transition-colors group">
<div class="flex items-center space-x-3">
<span class="flex items-center justify-center w-6 h-6 rounded-full border border-slate-300 dark:border-slate-600 text-xs text-slate-400">5</span>
<span class="font-medium">Wal-Muhsanat</span>
</div>
</button>
</div>
<div class="p-4 border-t border-slate-200 dark:border-slate-700/30 bg-slate-50/50 dark:bg-surface-dark/50">
<div class="mb-4">
<label class="text-xs text-slate-500 mb-2 block">Audio Recitation</label>
<select class="w-full bg-white dark:bg-slate-800 border border-slate-300 dark:border-slate-600 rounded-lg text-sm p-2 text-slate-700 dark:text-slate-200 focus:ring-primary focus:border-primary">
<option>Arabic (Mishary Rashid)</option>
<option>Arabic + Urdu Translation</option>
<option>Arabic + English Translation</option>
</select>
</div>
<button class="w-full py-2.5 px-4 bg-gradient-to-r from-primary to-yellow-600 hover:from-yellow-500 hover:to-yellow-700 text-white dark:text-slate-900 font-bold rounded-lg shadow-lg shadow-primary/20 flex items-center justify-center space-x-2 transition-all transform hover:scale-[1.02]">
<span class="material-icons-round text-sm">play_arrow</span>
<span>Smart Resume</span>
</button>
</div>
</aside>
<main class="flex-1 flex flex-col h-full overflow-hidden bg-[url('https://images.unsplash.com/photo-1590076215667-875d4ef2d743?ixlib=rb-4.0.3&amp;auto=format&amp;fit=crop&amp;w=2000&amp;q=80')] bg-cover bg-center">
<div class="absolute inset-0 bg-background-light/90 dark:bg-background-dark/90 pointer-events-none z-0"></div>
<header class="h-16 flex items-center justify-between px-8 border-b border-slate-200 dark:border-slate-700/30 glass-panel z-10 w-full">
<div class="flex items-center space-x-4">
<span class="text-sm font-semibold text-primary uppercase tracking-widest">Ramadan Day 12</span>
<span class="h-4 w-px bg-slate-300 dark:bg-slate-600"></span>
<h2 class="text-lg text-slate-800 dark:text-white font-serif">Surah Al-Baqarah <span class="text-slate-400 text-base font-sans font-normal ml-2">Verse 183-185</span></h2>
</div>
<div class="flex items-center space-x-4">
<button class="p-2 rounded-full text-slate-500 hover:text-primary transition-colors">
<span class="material-icons-round">bookmarks</span>
</button>
<button class="p-2 rounded-full text-slate-500 hover:text-primary transition-colors">
<span class="material-icons-round">settings</span>
</button>
<div class="w-8 h-8 rounded-full bg-emerald-deep flex items-center justify-center text-white text-xs font-bold ring-2 ring-primary ring-offset-2 ring-offset-background-dark">
                    HA
                </div>
</div>
</header>
<div class="flex-1 flex overflow-hidden z-10 p-6 gap-6">
<div class="flex-1 flex flex-col rounded-2xl glass-panel overflow-hidden shadow-2xl border border-slate-200 dark:border-slate-700/50">
<div class="flex-1 flex flex-row overflow-hidden relative">
<div class="absolute inset-0 opacity-5 pointer-events-none bg-[url('https://www.transparenttextures.com/patterns/arabesque.png')]"></div>
<div class="w-1/2 p-10 flex items-center justify-center border-r border-slate-200 dark:border-slate-700/30 bg-white/40 dark:bg-transparent">
<div class="text-center space-y-8">
<p class="font-arabic text-4xl leading-loose text-slate-800 dark:text-slate-100 drop-shadow-sm" dir="rtl">
                                يَا أَيُّهَا الَّذِينَ آمَنُوا كُتِبَ عَلَيْكُمُ الصِّيَامُ كَمَا كُتِبَ عَلَى الَّذِينَ مِن قَبْلِكُمْ لَعَلَّكُمْ تَتَّقُونَ
                            </p>
<div class="flex justify-center space-x-2">
<span class="w-2 h-2 rounded-full bg-primary/30"></span>
<span class="w-2 h-2 rounded-full bg-primary"></span>
<span class="w-2 h-2 rounded-full bg-primary/30"></span>
</div>
</div>
</div>
<div class="w-1/2 p-10 flex flex-col justify-center bg-slate-50/50 dark:bg-surface-dark/30">
<span class="text-primary text-xs font-bold uppercase tracking-wider mb-4">English Translation (Sahih International)</span>
<p class="text-xl leading-relaxed text-slate-700 dark:text-slate-300 font-serif mb-6">
                            "O you who have believed, decreed upon you is fasting as it was decreed upon those before you that you may become righteous."
                        </p>
<span class="text-primary text-xs font-bold uppercase tracking-wider mb-2 mt-4">Urdu Translation</span>
<p class="text-lg leading-relaxed text-slate-600 dark:text-slate-400 font-arabic dir-rtl text-right">
                            اے ایمان والو! تم پر روزے فرض کیے گئے جیسے تم سے پہلے لوگوں پر فرض کیے گئے تھے تاکہ تم پرہیزگار بن جاؤ۔
                        </p>
</div>
</div>
<div class="h-24 bg-white dark:bg-surface-dark border-t border-primary/20 flex flex-col justify-center px-8 relative">
<div class="absolute top-0 left-0 right-0 h-1 bg-slate-200 dark:bg-slate-700">
<div class="h-full bg-primary w-1/3 relative">
<div class="absolute right-0 -top-1 w-3 h-3 bg-white border-2 border-primary rounded-full shadow"></div>
</div>
</div>
<div class="flex items-center justify-between">
<div class="flex items-center space-x-6">
<button class="text-slate-400 hover:text-white transition-colors"><span class="material-icons-round">skip_previous</span></button>
<button class="w-12 h-12 rounded-full bg-primary text-white dark:text-surface-dark flex items-center justify-center shadow-lg hover:bg-yellow-500 transition-colors">
<span class="material-icons-round text-3xl">pause</span>
</button>
<button class="text-slate-400 hover:text-white transition-colors"><span class="material-icons-round">skip_next</span></button>
<div class="ml-4 text-sm font-mono text-primary">00:45 <span class="text-slate-500">/ 03:12</span></div>
</div>
<div class="flex-1 px-12 flex items-center justify-center space-x-1 h-8">
<div class="w-1 h-3 bg-primary/20 rounded-full"></div>
<div class="w-1 h-5 bg-primary/40 rounded-full"></div>
<div class="w-1 h-8 bg-primary rounded-full animate-pulse"></div>
<div class="w-1 h-4 bg-primary/40 rounded-full"></div>
<div class="w-1 h-6 bg-primary/60 rounded-full"></div>
<div class="w-1 h-3 bg-primary/20 rounded-full"></div>
<div class="w-1 h-8 bg-primary rounded-full animate-pulse delay-75"></div>
<div class="w-1 h-5 bg-primary/40 rounded-full"></div>
<div class="w-1 h-3 bg-primary/20 rounded-full"></div>
<div class="w-1 h-5 bg-primary/40 rounded-full"></div>
<div class="w-1 h-8 bg-primary rounded-full animate-pulse"></div>
<div class="w-1 h-4 bg-primary/40 rounded-full"></div>
<div class="w-1 h-3 bg-primary/20 rounded-full"></div>
<div class="w-1 h-5 bg-primary/40 rounded-full"></div>
<div class="w-1 h-8 bg-primary rounded-full animate-pulse"></div>
<div class="w-1 h-4 bg-primary/40 rounded-full"></div>
</div>
<div class="flex items-center space-x-4">
<button class="text-slate-400 hover:text-primary transition-colors flex items-center gap-1 text-xs uppercase tracking-wide border border-slate-700 px-2 py-1 rounded">
<span class="material-icons-round text-sm">speed</span> 1.0x
                            </button>
<button class="text-slate-400 hover:text-primary transition-colors">
<span class="material-icons-round">repeat</span>
</button>
</div>
</div>
</div>
</div>
<aside class="w-96 flex flex-col rounded-2xl glass-panel border border-slate-200 dark:border-slate-700/50 shadow-2xl relative overflow-hidden">
<div class="p-4 border-b border-slate-200 dark:border-slate-700/30 flex items-center justify-between bg-white/50 dark:bg-surface-dark/50 backdrop-blur-sm">
<div class="flex items-center space-x-3">
<div class="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg">
<span class="material-icons-round text-white text-sm">psychology</span>
</div>
<div>
<h3 class="text-sm font-bold text-slate-800 dark:text-white">Scholar Agent</h3>
<span class="text-[10px] text-emerald-500 flex items-center gap-1">
<span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span> Online
                            </span>
</div>
</div>
<button class="text-slate-400 hover:text-primary"><span class="material-icons-round text-lg">more_horiz</span></button>
</div>
<div class="flex-1 overflow-y-auto p-4 space-y-4 bg-slate-50/50 dark:bg-transparent">
<div class="flex flex-col space-y-2">
<div class="flex items-center space-x-2 text-xs text-slate-500 dark:text-slate-400 ml-1">
<span class="font-bold text-primary">Hidayah AI</span>
<span>12:45 PM</span>
</div>
<div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-4 rounded-2xl rounded-tl-none shadow-sm text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
<p>Assalamu Alaykum. Based on Surah Al-Baqarah Verse 183, would you like to explore the Tafsir regarding the historical context of fasting in pre-Islamic nations, or focus on the spiritual benefits mentioned by Imam Al-Ghazali?</p>
</div>
</div>
<div class="flex flex-col space-y-2 items-end">
<div class="flex items-center space-x-2 text-xs text-slate-500 dark:text-slate-400 mr-1">
<span>You</span>
<span>12:46 PM</span>
</div>
<div class="bg-primary/20 border border-primary/30 p-4 rounded-2xl rounded-tr-none shadow-sm text-sm text-slate-800 dark:text-slate-100 leading-relaxed max-w-[90%]">
<p>Can you summarize the fiqh rulings related to travel exemptions mentioned in the subsequent verses?</p>
</div>
</div>
<div class="flex flex-col space-y-2 animate-pulse">
<div class="flex items-center space-x-2 text-xs text-slate-500 dark:text-slate-400 ml-1">
<span class="font-bold text-primary">Hidayah AI</span>
<span class="text-emerald-500 flex items-center gap-1 text-[10px] border border-emerald-500/30 px-1.5 py-0.5 rounded-full bg-emerald-500/10">
<span class="material-icons-round text-[10px]">travel_explore</span>
                                Selecting Web Research Tool...
                            </span>
</div>
<div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-4 rounded-2xl rounded-tl-none shadow-sm w-3/4">
<div class="h-2 bg-slate-200 dark:bg-slate-700 rounded w-full mb-2"></div>
<div class="h-2 bg-slate-200 dark:bg-slate-700 rounded w-2/3"></div>
</div>
</div>
</div>
<div class="p-4 bg-white dark:bg-surface-dark border-t border-slate-200 dark:border-slate-700/50">
<div class="relative">
<textarea class="w-full bg-slate-100 dark:bg-slate-900 border-none rounded-xl p-3 pl-4 pr-12 text-sm text-slate-800 dark:text-white placeholder-slate-400 focus:ring-2 focus:ring-primary resize-none h-14 shadow-inner" placeholder="Ask a question about this verse..."></textarea>
<div class="absolute right-2 bottom-2 flex items-center space-x-1">
<button class="p-1.5 text-slate-400 hover:text-primary transition-colors rounded-lg hover:bg-slate-200 dark:hover:bg-slate-800" title="Upload PDF">
<span class="material-icons-round text-lg">attach_file</span>
</button>
<button class="p-1.5 bg-primary text-white dark:text-slate-900 rounded-lg shadow-md hover:bg-yellow-500 transition-colors">
<span class="material-icons-round text-lg">send</span>
</button>
</div>
</div>
<div class="mt-2 flex justify-center">
<span class="text-[10px] text-slate-400">AI can make mistakes. Verify with scholars.</span>
</div>
</div>
</aside>
</div>
</main>

</body></html>