"""
Seed marketing legends with their cognitive clones
"""
from models import ExpertCreate, ExpertType, CategoryType
from storage import MemStorage
from prompts.legends import LEGENDS_PROMPTS

async def seed_legends(storage: MemStorage):
    """Seed the 18 marketing & growth experts as high-fidelity cognitive clones"""
    
    legends_data = [
        # MARKETING CATEGORY (Traditional marketing legends)
        {
            "name": "Philip Kotler",
            "title": "O Pai do Marketing Moderno",
            "bio": "Professor, autor e consultor considerado o maior especialista mundial em marketing estratégico. Criador dos 4Ps e pioneiro em segmentação de mercado.",
            "expertise": ["Estratégia de Marketing", "Segmentação", "4Ps", "Brand Positioning", "Marketing Internacional"],
            "system_prompt": LEGENDS_PROMPTS["philip_kotler"],
            "avatar": "/attached_assets/generated_images/Philip_Kotler_professional_portrait_bbb250dd.png",
            "category": CategoryType.MARKETING,
        },
        {
            "name": "David Ogilvy",
            "title": "O Pai da Publicidade",
            "bio": "Fundador da Ogilvy & Mather, criou campanhas icônicas e revolucionou o copywriting. Mestre em construir marcas de luxo e comunicação persuasiva.",
            "expertise": ["Copywriting", "Brand Building", "Direct Response", "Creative Strategy", "Luxury Marketing"],
            "system_prompt": LEGENDS_PROMPTS["david_ogilvy"],
            "avatar": "/attached_assets/generated_images/David_Ogilvy_1960s_portrait_322198ff.png",
            "category": CategoryType.MARKETING,
        },
        {
            "name": "Claude C. Hopkins",
            "title": "Pioneiro do Marketing Científico",
            "bio": "Revolucionou a publicidade no início do século XX ao introduzir testes mensuráveis e rastreamento de ROI. Autor de 'Scientific Advertising'.",
            "expertise": ["Scientific Advertising", "A/B Testing", "ROI Tracking", "Direct Response", "Teste e Mensuração"],
            "system_prompt": LEGENDS_PROMPTS["claude_hopkins"],
            "avatar": "/attached_assets/generated_images/Claude_Hopkins_vintage_portrait_b074ce60.png",
            "category": CategoryType.MARKETING,
        },
        {
            "name": "John Wanamaker",
            "title": "Revolucionário do Varejo Moderno",
            "bio": "Pioneiro do varejo moderno, criou a garantia de devolução e revolucionou o marketing de massa. Famoso pela frase sobre metade do orçamento publicitário.",
            "expertise": ["Retail Strategy", "Customer Trust", "Print Advertising", "Garantia de Devolução", "Mass Marketing"],
            "system_prompt": LEGENDS_PROMPTS["john_wanamaker"],
            "avatar": "/attached_assets/generated_images/John_Wanamaker_Victorian_portrait_9fe2f89b.png",
            "category": CategoryType.MARKETING,
        },
        {
            "name": "Mary Wells Lawrence",
            "title": "Pioneira do Branding Emocional",
            "bio": "Primeira mulher CEO de uma agência na NYSE, criou campanhas emocionais icônicas como 'I ♥ NY'. Revolucionou o lifestyle marketing e branding de moda.",
            "expertise": ["Branding Emocional", "Lifestyle Marketing", "Fashion Advertising", "I ♥ NY", "Creative Leadership"],
            "system_prompt": LEGENDS_PROMPTS["mary_wells_lawrence"],
            "avatar": "/attached_assets/generated_images/Mary_Wells_Lawrence_portrait_ee4b7088.png",
            "category": CategoryType.MARKETING,
        },
        {
            "name": "Leo Burnett",
            "title": "O Rei do Storytelling Publicitário",
            "bio": "Fundador da Leo Burnett Worldwide, criou personagens arquetípicos icônicos como o Marlboro Man. Mestre em encontrar o 'inherent drama' de produtos.",
            "expertise": ["Storytelling", "Archetypal Characters", "Inherent Drama", "Visual Branding", "Marlboro Man"],
            "system_prompt": LEGENDS_PROMPTS["leo_burnett"],
            "avatar": "/attached_assets/generated_images/Leo_Burnett_classic_portrait_e1f25f37.png",
            "category": CategoryType.MARKETING,
        },
        
        # POSITIONING CATEGORY
        {
            "name": "Al Ries & Jack Trout",
            "title": "Os Arquitetos do Posicionamento Estratégico",
            "bio": "Dupla lendária que criou as 22 Leis Imutáveis do Marketing e revolucionou o conceito de posicionamento. Foco laser em ocupar posição única na mente do consumidor.",
            "expertise": ["Posicionamento", "22 Leis Imutáveis", "First-Mover Advantage", "Foco Estratégico", "Mente do Consumidor"],
            "system_prompt": LEGENDS_PROMPTS["al_ries_jack_trout"],
            "avatar": None,  # Will generate later
            "category": CategoryType.POSITIONING,
        },
        
        # CREATIVE CATEGORY
        {
            "name": "Bill Bernbach",
            "title": "O Revolucionário Criativo",
            "bio": "Co-fundador da DDB, liderou a Creative Revolution dos anos 60. Criou campanhas icônicas como 'Think Small' da Volkswagen e transformou publicidade em arte.",
            "expertise": ["Creative Revolution", "Art + Copy Partnership", "Think Small", "Avis Campaign", "Breakthrough Ideas"],
            "system_prompt": LEGENDS_PROMPTS["bill_bernbach"],
            "avatar": None,
            "category": CategoryType.CREATIVE,
        },
        
        # DIRECT RESPONSE CATEGORY
        {
            "name": "Dan Kennedy",
            "title": "O Rei do Direct Response Marketing",
            "bio": "Copywriter lendário e consultor multi-milionário. Criador do Magnetic Marketing e das 10 Commandments of Copy. Mestre em funis de conversão e maximização de LTV.",
            "expertise": ["Direct Response", "Magnetic Marketing", "Sales Letters", "Maximização LTV", "Copywriting de Conversão"],
            "system_prompt": LEGENDS_PROMPTS["dan_kennedy"],
            "avatar": None,
            "category": CategoryType.DIRECT_RESPONSE,
        },
        
        # CONTENT CATEGORY
        {
            "name": "Seth Godin",
            "title": "Visionário do Permission Marketing",
            "bio": "Autor best-seller e guru do marketing moderno. Criador dos conceitos Purple Cow e Tribes, pioneiro em permission marketing e storytelling digital.",
            "expertise": ["Permission Marketing", "Purple Cow", "Tribes", "Storytelling Digital", "Nicho e Posicionamento"],
            "system_prompt": LEGENDS_PROMPTS["seth_godin"],
            "avatar": "/attached_assets/generated_images/Seth_Godin_modern_portrait_1b27fbc0.png",
            "category": CategoryType.CONTENT,
        },
        {
            "name": "Ann Handley",
            "title": "A Rainha do Content Marketing",
            "bio": "Chief Content Officer da MarketingProfs, autora best-seller de 'Everybody Writes'. Pioneira em content marketing e evangelista de writing com empatia e utilidade extrema.",
            "expertise": ["Content Marketing", "Everybody Writes", "Brand Voice", "Editorial Strategy", "Human Writing"],
            "system_prompt": LEGENDS_PROMPTS["ann_handley"],
            "avatar": None,
            "category": CategoryType.CONTENT,
        },
        
        # SEO CATEGORY
        {
            "name": "Neil Patel",
            "title": "O Mestre do SEO Data-Driven",
            "bio": "Co-fundador da NP Digital e Ubersuggest, reconhecido como top influencer em digital marketing. Expert em SEO, content marketing e growth hacking orientado por dados.",
            "expertise": ["SEO", "Ubersuggest", "Content Decay", "Technical SEO", "Data-Driven Marketing"],
            "system_prompt": LEGENDS_PROMPTS["neil_patel"],
            "avatar": None,
            "category": CategoryType.SEO,
        },
        
        # SOCIAL CATEGORY
        {
            "name": "Gary Vaynerchuk",
            "title": "Rei do Marketing Digital e Hustle",
            "bio": "Empreendedor serial, investidor e especialista em redes sociais. Conhecido por sua abordagem direta, foco em personal branding e 'day trading attention'.",
            "expertise": ["Social Media", "Personal Branding", "Day Trading Attention", "Content Creation", "Entrepreneurship"],
            "system_prompt": LEGENDS_PROMPTS["gary_vaynerchuk"],
            "avatar": "/attached_assets/generated_images/Gary_Vaynerchuk_entrepreneur_portrait_0501810f.png",
            "category": CategoryType.SOCIAL,
        },
        
        # GROWTH CATEGORY (Growth hackers)
        {
            "name": "Sean Ellis",
            "title": "O Criador do Growth Hacking",
            "bio": "Criador do termo 'growth hacking', autor de 'Hacking Growth'. Desenvolveu o ICE Framework e a 40% Rule para Product-Market Fit. Ex-Head of Growth da Dropbox.",
            "expertise": ["Growth Hacking", "ICE Framework", "40% Rule PMF", "Dropbox Referral", "Activation Optimization"],
            "system_prompt": LEGENDS_PROMPTS["sean_ellis"],
            "avatar": None,
            "category": CategoryType.GROWTH,
        },
        {
            "name": "Brian Balfour",
            "title": "O Arquiteto de Growth Systems",
            "bio": "Founder & CEO da Reforge, ex-VP Growth @ HubSpot. Criador do Four Fits Framework e defensor de Growth Loops vs Funnels. Revolucionou educação em growth.",
            "expertise": ["Four Fits Framework", "Growth Loops", "Market-Product Fit", "Reforge", "Strategic Alignment"],
            "system_prompt": LEGENDS_PROMPTS["brian_balfour"],
            "avatar": None,
            "category": CategoryType.GROWTH,
        },
        {
            "name": "Andrew Chen",
            "title": "O Especialista em Network Effects",
            "bio": "General Partner @ Andreessen Horowitz, ex-Head of Rider Growth @ Uber. Autor de 'The Cold Start Problem'. Expert em network effects e marketplace dynamics.",
            "expertise": ["Network Effects", "Cold Start Problem", "Marketplace Dynamics", "Atomic Networks", "Uber Growth"],
            "system_prompt": LEGENDS_PROMPTS["andrew_chen"],
            "avatar": None,
            "category": CategoryType.GROWTH,
        },
        
        # VIRAL CATEGORY
        {
            "name": "Jonah Berger",
            "title": "O Cientista da Viralidade",
            "bio": "Professor @ Wharton, autor de 'Contagious: Why Things Catch On'. Criador do STEPPS Framework. Expert em word-of-mouth e viral marketing baseado em ciência.",
            "expertise": ["STEPPS Framework", "Viral Marketing", "Word-of-Mouth", "Contagious Content", "Social Currency"],
            "system_prompt": LEGENDS_PROMPTS["jonah_berger"],
            "avatar": None,
            "category": CategoryType.VIRAL,
        },
        
        # PRODUCT CATEGORY
        {
            "name": "Nir Eyal",
            "title": "O Especialista em Habit Formation",
            "bio": "Behavioral economist, autor de 'Hooked: How to Build Habit-Forming Products'. Criador do Hooked Model (Trigger-Action-Reward-Investment). Professor @ Stanford GSB.",
            "expertise": ["Hooked Model", "Habit Formation", "Behavioral Design", "Hook Canvas", "Variable Rewards"],
            "system_prompt": LEGENDS_PROMPTS["nir_eyal"],
            "avatar": None,
            "category": CategoryType.PRODUCT,
        },
    ]
    
    for legend in legends_data:
        expert_data = ExpertCreate(
            name=legend["name"],
            title=legend["title"],
            bio=legend["bio"],
            expertise=legend["expertise"],
            systemPrompt=legend["system_prompt"],
            avatar=legend["avatar"],
            category=legend["category"],
            expertType=ExpertType.HIGH_FIDELITY  # These are high-fidelity clones
        )
        await storage.create_expert(expert_data)
