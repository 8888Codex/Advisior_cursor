"""
Seed marketing legends with their cognitive clones
"""
from models import ExpertCreate, ExpertType
from storage import MemStorage
from prompts.legends import LEGENDS_PROMPTS

async def seed_legends(storage: MemStorage):
    """Seed the 8 marketing legends as high-fidelity cognitive clones"""
    
    legends_data = [
        {
            "name": "Philip Kotler",
            "title": "O Pai do Marketing Moderno",
            "bio": "Professor, autor e consultor considerado o maior especialista mundial em marketing estratégico. Criador dos 4Ps e pioneiro em segmentação de mercado.",
            "expertise": ["Estratégia de Marketing", "Segmentação", "4Ps", "Brand Positioning", "Marketing Internacional"],
            "system_prompt": LEGENDS_PROMPTS["philip_kotler"],
            "avatar": "/attached_assets/generated_images/Philip_Kotler_professional_portrait_bbb250dd.png",
            "prompt_key": "philip_kotler"
        },
        {
            "name": "David Ogilvy",
            "title": "O Pai da Publicidade",
            "bio": "Fundador da Ogilvy & Mather, criou campanhas icônicas e revolucionou o copywriting. Mestre em construir marcas de luxo e comunicação persuasiva.",
            "expertise": ["Copywriting", "Brand Building", "Direct Response", "Creative Strategy", "Luxury Marketing"],
            "system_prompt": LEGENDS_PROMPTS["david_ogilvy"],
            "avatar": "/attached_assets/generated_images/David_Ogilvy_1960s_portrait_322198ff.png",
            "prompt_key": "david_ogilvy"
        },
        {
            "name": "Claude C. Hopkins",
            "title": "Pioneiro do Marketing Científico",
            "bio": "Revolucionou a publicidade no início do século XX ao introduzir testes mensuráveis e rastreamento de ROI. Autor de 'Scientific Advertising'.",
            "expertise": ["Scientific Advertising", "A/B Testing", "ROI Tracking", "Direct Response", "Teste e Mensuração"],
            "system_prompt": LEGENDS_PROMPTS["claude_hopkins"],
            "avatar": "/attached_assets/generated_images/Claude_Hopkins_vintage_portrait_b074ce60.png",
            "prompt_key": "claude_hopkins"
        },
        {
            "name": "John Wanamaker",
            "title": "Revolucionário do Varejo Moderno",
            "bio": "Pioneiro do varejo moderno, criou a garantia de devolução e revolucionou o marketing de massa. Famoso pela frase sobre metade do orçamento publicitário.",
            "expertise": ["Retail Strategy", "Customer Trust", "Print Advertising", "Garantia de Devolução", "Mass Marketing"],
            "system_prompt": LEGENDS_PROMPTS["john_wanamaker"],
            "avatar": "/attached_assets/generated_images/John_Wanamaker_Victorian_portrait_9fe2f89b.png",
            "prompt_key": "john_wanamaker"
        },
        {
            "name": "Mary Wells Lawrence",
            "title": "Pioneira do Branding Emocional",
            "bio": "Primeira mulher CEO de uma agência na NYSE, criou campanhas emocionais icônicas como 'I ♥ NY'. Revolucionou o lifestyle marketing e branding de moda.",
            "expertise": ["Branding Emocional", "Lifestyle Marketing", "Fashion Advertising", "I ♥ NY", "Creative Leadership"],
            "system_prompt": LEGENDS_PROMPTS["mary_wells_lawrence"],
            "avatar": "/attached_assets/generated_images/Mary_Wells_Lawrence_portrait_ee4b7088.png",
            "prompt_key": "mary_wells_lawrence"
        },
        {
            "name": "Seth Godin",
            "title": "Visionário do Permission Marketing",
            "bio": "Autor best-seller e guru do marketing moderno. Criador dos conceitos Purple Cow e Tribes, pioneiro em permission marketing e storytelling digital.",
            "expertise": ["Permission Marketing", "Purple Cow", "Tribes", "Storytelling Digital", "Nicho e Posicionamento"],
            "system_prompt": LEGENDS_PROMPTS["seth_godin"],
            "avatar": "/attached_assets/generated_images/Seth_Godin_modern_portrait_1b27fbc0.png",
            "prompt_key": "seth_godin"
        },
        {
            "name": "Gary Vaynerchuk",
            "title": "Rei do Marketing Digital e Hustle",
            "bio": "Empreendedor serial, investidor e especialista em redes sociais. Conhecido por sua abordagem direta, foco em personal branding e 'day trading attention'.",
            "expertise": ["Social Media", "Personal Branding", "Day Trading Attention", "Content Creation", "Entrepreneurship"],
            "system_prompt": LEGENDS_PROMPTS["gary_vaynerchuk"],
            "avatar": "/attached_assets/generated_images/Gary_Vaynerchuk_entrepreneur_portrait_0501810f.png",
            "prompt_key": "gary_vaynerchuk"
        },
        {
            "name": "Leo Burnett",
            "title": "O Rei do Storytelling Publicitário",
            "bio": "Fundador da Leo Burnett Worldwide, criou personagens arquetípicos icônicos como o Marlboro Man. Mestre em encontrar o 'inherent drama' de produtos.",
            "expertise": ["Storytelling", "Archetypal Characters", "Inherent Drama", "Visual Branding", "Marlboro Man"],
            "system_prompt": LEGENDS_PROMPTS["leo_burnett"],
            "avatar": "/attached_assets/generated_images/Leo_Burnett_classic_portrait_e1f25f37.png",
            "prompt_key": "leo_burnett"
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
            expertType=ExpertType.HIGH_FIDELITY  # These are high-fidelity clones
        )
        await storage.create_expert(expert_data)
