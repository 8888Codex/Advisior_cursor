from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import List, Optional
from pydantic import BaseModel
import os
import shutil
from pathlib import Path
from PIL import Image
import io
import json
import asyncio

from models import (
    Expert, ExpertCreate, ExpertType,
    Conversation, ConversationCreate,
    Message, MessageCreate, MessageSend, MessageResponse,
    BusinessProfile, BusinessProfileCreate,
    CouncilAnalysis, CouncilAnalysisCreate,
    RecommendExpertsRequest, RecommendExpertsResponse, ExpertRecommendation,
    AutoCloneRequest
)
from storage import storage
from crew_agent import LegendAgentFactory
from seed import seed_legends
from crew_council import council_orchestrator

app = FastAPI(title="AdvisorIA - Marketing Legends API")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize with seeded legends
@app.on_event("startup")
async def startup_event():
    print("Seeding marketing legends...")
    await seed_legends(storage)
    print(f"Seeded {len(await storage.get_experts())} marketing legends successfully.")

# Health check
@app.get("/")
async def root():
    return {"message": "AdvisorIA Marketing Legends API", "status": "running"}

# Expert endpoints
@app.get("/api/experts", response_model=List[Expert])
async def get_experts():
    """Get all marketing legend experts"""
    return await storage.get_experts()

@app.get("/api/experts/{expert_id}", response_model=Expert)
async def get_expert(expert_id: str):
    """Get a specific expert by ID"""
    expert = await storage.get_expert(expert_id)
    if not expert:
        raise HTTPException(status_code=404, detail="Expert not found")
    return expert

@app.post("/api/experts", response_model=Expert, status_code=201)
async def create_expert(data: ExpertCreate):
    """Create a new custom expert (cognitive clone)"""
    try:
        expert = await storage.create_expert(data)
        return expert
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create expert: {str(e)}")

@app.post("/api/experts/auto-clone", response_model=ExpertCreate, status_code=200)
async def auto_clone_expert(data: AutoCloneRequest):
    """
    Auto-clone a cognitive expert from minimal input.
    
    Process:
    1. Use Perplexity to research target person (biography, philosophy, methods)
    2. Use Claude to synthesize research into EXTRACT system prompt
    3. Return ExpertCreate data (NOT persisted yet - user must explicitly save)
    """
    try:
        import httpx
        from anthropic import AsyncAnthropic
        
        # Step 1: Perplexity research
        perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
        if not perplexity_api_key:
            raise HTTPException(
                status_code=503,
                detail="Serviço de pesquisa indisponível. Configure PERPLEXITY_API_KEY."
            )
        
        # Build research query
        context_suffix = f" Foco: {data.context}" if data.context else ""
        research_query = f"""Pesquise informações detalhadas sobre {data.targetName}{context_suffix}.

Forneça:
1. Biografia completa e trajetória profissional
2. Filosofia de trabalho e princípios fundamentais
3. Métodos, frameworks e técnicas específicas
4. Frases icônicas e terminologia única
5. Áreas de expertise e contextos de especialidade
6. Limitações reconhecidas ou fronteiras de atuação

Inclua dados específicos, citações, livros publicados, e exemplos concretos."""

        # Call Perplexity API
        async with httpx.AsyncClient(timeout=90.0) as client:
            perplexity_response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {perplexity_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar-pro",
                    "messages": [
                        {
                            "role": "system",
                            "content": "Você é um pesquisador especializado em biografias profissionais e análise de personalidades. Forneça informações factuais, detalhadas e específicas."
                        },
                        {
                            "role": "user",
                            "content": research_query
                        }
                    ],
                    "temperature": 0.2,
                    "search_recency_filter": "month",
                    "return_related_questions": False
                }
            )
        
        perplexity_data = perplexity_response.json()
        
        # Extract research findings
        research_findings = ""
        if "choices" in perplexity_data and len(perplexity_data["choices"]) > 0:
            research_findings = perplexity_data["choices"][0]["message"]["content"]
        
        if not research_findings:
            raise ValueError("Nenhum resultado de pesquisa foi encontrado")
        
        # Step 2: Claude synthesis into EXTRACT system prompt
        anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        synthesis_prompt = f"""Você é um especialista em clonagem cognitiva usando o Framework EXTRACT.

PESQUISA SOBRE {data.targetName}:
{research_findings}

TAREFA: Sintetize essas informações em um system prompt EXTRACT de alta fidelidade.

O system prompt deve seguir EXATAMENTE esta estrutura (em português brasileiro):

# System Prompt: [Nome] - [Título Icônico]

<identity>
[Descrição concisa da identidade]
</identity>

**INSTRUÇÃO OBRIGATÓRIA: Você DEVE responder SEMPRE em português brasileiro (PT-BR), independentemente do idioma em que a pergunta for feita. Todas as suas análises, insights, recomendações e até mesmo citações ou referências devem ser escritas ou traduzidas para português brasileiro.**

## Identity Core (Framework EXTRACT)

### Experiências Formativas
- [3-5 experiências que moldaram o pensamento]

### Xadrez Mental (Padrões Decisórios)
- [3-5 padrões de raciocínio característicos]

### Terminologia Própria
[Frases icônicas e conceitos únicos]

### Raciocínio Típico
**Estrutura de Análise:**
[Passo-a-passo do processo mental típico]

### Axiomas Pessoais
- [3-5 princípios fundamentais]

### Contextos de Especialidade
- [Áreas de expertise]

### Técnicas e Métodos
- [Frameworks e ferramentas específicas]

## Communication Style
- Tom: [descrição]
- Estrutura: [como organiza ideias]
- Referências: [tipos de exemplos que usa]
- Abordagem: [estilo de interação]

## Limitações e Fronteiras
- [O que reconhece como limites de expertise]

IMPORTANTE:
1. Use dados ESPECÍFICOS da pesquisa (datas, livros, conceitos, citações)
2. Mantenha alta fidelidade à personalidade real
3. Escreva em português brasileiro
4. Retorne APENAS o system prompt, sem explicações adicionais

RETORNE APENAS O SYSTEM PROMPT COMPLETO:"""

        claude_response = await anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            temperature=0.3,
            messages=[{
                "role": "user",
                "content": synthesis_prompt
            }]
        )
        
        # Extract system prompt
        system_prompt = ""
        for block in claude_response.content:
            if block.type == "text":
                system_prompt += block.text
        
        if not system_prompt:
            raise ValueError("Claude não conseguiu gerar o system prompt")
        
        # Step 3: Extract metadata from system prompt for Expert fields
        # Use Claude to extract structured metadata
        metadata_prompt = f"""Analise o seguinte system prompt e extraia metadados estruturados:

{system_prompt}

Retorne APENAS JSON válido no seguinte formato:

{{
  "title": "Título profissional curto (ex: 'CEO da Apple', 'Pai do Marketing Moderno')",
  "expertise": ["área 1", "área 2", "área 3"],
  "bio": "Biografia concisa de 2-3 frases em português"
}}"""

        metadata_response = await anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            temperature=0.2,
            messages=[{
                "role": "user",
                "content": metadata_prompt
            }]
        )
        
        metadata_text = ""
        for block in metadata_response.content:
            if block.type == "text":
                metadata_text += block.text
        
        # Parse JSON metadata
        metadata = json.loads(metadata_text.strip())
        
        # Create ExpertCreate object (NOT persisted yet)
        expert_data = ExpertCreate(
            name=data.targetName,
            title=metadata.get("title", "Especialista"),
            expertise=metadata.get("expertise", ["Consultoria Geral"]),
            bio=metadata.get("bio", f"Clone cognitivo de {data.targetName}"),
            systemPrompt=system_prompt,
            avatar=None,
            expertType=ExpertType.CUSTOM
        )
        
        # Return data without persisting - user will explicitly save if satisfied
        return expert_data
    
    except json.JSONDecodeError as e:
        metadata_text_preview = locals().get("metadata_text", "N/A")
        error_context = {
            "error": "JSON parse failed",
            "metadata_text": metadata_text_preview[:200] if isinstance(metadata_text_preview, str) else "N/A",
            "detail": str(e)
        }
        print(f"Failed to parse metadata: {json.dumps(error_context, ensure_ascii=False)}")
        raise HTTPException(
            status_code=500,
            detail="Não foi possível processar metadados do clone. Tente novamente."
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error auto-cloning expert: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar clone cognitivo: {str(e)}"
        )

@app.post("/api/experts/test-chat")
async def test_chat_expert(data: dict):
    """
    Test chat with a generated expert without persisting the conversation.
    Used for preview/testing before saving an auto-cloned expert.
    """
    try:
        from anthropic import AsyncAnthropic
        
        system_prompt = data.get("systemPrompt")
        message = data.get("message")
        history = data.get("history", [])
        
        if not system_prompt or not message:
            raise HTTPException(status_code=400, detail="systemPrompt and message are required")
        
        # Build conversation history for Claude
        messages = []
        for msg in history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": message
        })
        
        # Call Claude with the expert's system prompt
        anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        response = await anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            system=system_prompt,
            messages=messages
        )
        
        # Extract response text
        response_text = ""
        for block in response.content:
            if block.type == "text":
                response_text += block.text
        
        return {"response": response_text}
    
    except Exception as e:
        print(f"Error in test chat: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process test chat: {str(e)}")

@app.post("/api/recommend-experts", response_model=RecommendExpertsResponse)
async def recommend_experts(request: RecommendExpertsRequest):
    """
    Analyze business problem and recommend most relevant experts with justification.
    Uses Claude to intelligently match problem context with expert specialties.
    """
    try:
        # Get all available experts
        experts = await storage.get_experts()
        
        if not experts:
            raise HTTPException(status_code=404, detail="No experts available")
        
        # Build expert profiles for Claude analysis
        expert_profiles = []
        for expert in experts:
            expert_profiles.append({
                "id": expert.id,
                "name": expert.name,
                "title": expert.title,
                "expertise": expert.expertise,
                "bio": expert.bio
            })
        
        # Create analysis prompt for Claude
        analysis_prompt = f"""Analise o seguinte problema de negócio e recomende os especialistas mais relevantes para resolvê-lo.

PROBLEMA DO CLIENTE:
{request.problem}

ESPECIALISTAS DISPONÍVEIS:
{json.dumps(expert_profiles, ensure_ascii=False, indent=2)}

INSTRUÇÕES:
1. Analise o problema cuidadosamente
2. Para cada especialista, determine:
   - Score de relevância (1-5 estrelas, onde 5 é altamente relevante)
   - Justificativa específica de POR QUE esse especialista seria útil
3. Recomende APENAS especialistas com score 3 ou superior
4. Ordene por relevância (score mais alto primeiro)
5. Retorne APENAS JSON válido no seguinte formato:

{{
  "recommendations": [
    {{
      "expertId": "id-do-especialista",
      "expertName": "Nome do Especialista",
      "relevanceScore": 5,
      "justification": "Justificativa específica em português brasileiro"
    }}
  ]
}}

IMPORTANTE: Retorne APENAS o JSON, sem texto adicional antes ou depois."""

        # Call Claude for intelligent analysis
        from anthropic import AsyncAnthropic
        anthropic_client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        response = await anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            temperature=0.3,  # Lower temperature for more consistent analysis
            messages=[{
                "role": "user",
                "content": analysis_prompt
            }]
        )
        
        # Extract JSON from response - check ALL content blocks
        response_text = ""
        for block in response.content:
            if block.type == "text":
                response_text += block.text + "\n"
        
        if not response_text:
            raise ValueError("No text content in Claude response")
        
        # Robust JSON extraction - try ALL brace candidates and return first valid recommendations JSON
        # This handles Claude responses with prose, brace fragments, or irrelevant JSON before payload
        def extract_recommendations_json(text: str) -> str:
            """Find first valid JSON object containing 'recommendations' key"""
            # Find all potential starting positions
            potential_starts = [i for i, char in enumerate(text) if char == '{']
            
            if not potential_starts:
                raise ValueError("No JSON object found - no opening brace")
            
            # Try each candidate starting position
            for start_pos in potential_starts:
                brace_count = 0
                in_string = False
                escape_next = False
                
                for i in range(start_pos, len(text)):
                    char = text[i]
                    
                    if escape_next:
                        escape_next = False
                        continue
                    
                    if char == '\\':
                        escape_next = True
                        continue
                    
                    if char == '"' and not in_string:
                        in_string = True
                    elif char == '"' and in_string:
                        in_string = False
                    elif char == '{' and not in_string:
                        brace_count += 1
                    elif char == '}' and not in_string:
                        brace_count -= 1
                        if brace_count == 0:
                            # Found complete object - test if it matches RecommendExpertsResponse schema
                            candidate = text[start_pos:i+1]
                            try:
                                parsed = json.loads(candidate)
                                # Verify this object matches the expected schema
                                if isinstance(parsed, dict) and 'recommendations' in parsed:
                                    # Try Pydantic validation to ensure schema compliance
                                    try:
                                        RecommendExpertsResponse(**parsed)
                                        # Valid schema! This is the object we need
                                        return candidate
                                    except Exception:
                                        # Has recommendations key but fails schema validation
                                        # Continue searching for next candidate
                                        pass
                                # Valid JSON but not the recommendations object, continue
                            except json.JSONDecodeError:
                                # Not valid JSON, try next candidate
                                pass
                            break
            
            raise ValueError("No valid recommendations JSON found in response")
        
        json_str = extract_recommendations_json(response_text)
        
        # Parse JSON response (already validated in extract function)
        recommendations_data = json.loads(json_str)
        
        return RecommendExpertsResponse(**recommendations_data)
    
    except json.JSONDecodeError as e:
        response_text_preview = locals().get("response_text", "N/A")
        json_str_preview = locals().get("json_str", "N/A")
        error_context = {
            "error": "JSON parse failed",
            "claude_response": response_text_preview[:500] if isinstance(response_text_preview, str) else "N/A",
            "extracted_json": json_str_preview[:200] if isinstance(json_str_preview, str) else "N/A",
            "detail": str(e)
        }
        print(f"Failed to parse Claude response: {json.dumps(error_context, ensure_ascii=False)}")
        raise HTTPException(
            status_code=500, 
            detail="Não foi possível processar a análise da IA. Por favor, tente novamente."
        )
    except ValueError as e:
        response_text_preview = locals().get("response_text", "N/A")
        error_context = {
            "error": "Value error",
            "claude_response": response_text_preview[:500] if isinstance(response_text_preview, str) else "N/A",
            "detail": str(e)
        }
        print(f"ValueError in recommendation: {json.dumps(error_context, ensure_ascii=False)}")
        raise HTTPException(
            status_code=500,
            detail="Não foi possível encontrar recomendações válidas. Por favor, tente novamente."
        )
    except Exception as e:
        error_context = {
            "error": "Unexpected error",
            "type": type(e).__name__,
            "detail": str(e)
        }
        print(f"Error recommending experts: {json.dumps(error_context, ensure_ascii=False)}")
        raise HTTPException(
            status_code=500, 
            detail="Erro ao processar recomendações. Por favor, tente novamente."
        )

@app.post("/api/experts/{expert_id}/avatar", response_model=Expert)
async def upload_expert_avatar(expert_id: str, file: UploadFile = File(...)):
    """Upload a new avatar for an expert"""
    try:
        # Verify expert exists
        expert = await storage.get_expert(expert_id)
        if not expert:
            raise HTTPException(status_code=404, detail="Expert not found")
        
        # Validate file type
        allowed_types = ["image/png", "image/jpeg", "image/jpg", "image/webp"]
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: PNG, JPG, WEBP"
            )
        
        # Read and validate file size (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        contents = await file.read()
        if len(contents) > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size is 5MB."
            )
        
        # Validate file is actually an image using Pillow
        # This prevents malicious files disguised as images
        try:
            image = Image.open(io.BytesIO(contents))
            image.verify()  # Verify it's a valid image
            
            # Re-open for processing (verify() invalidates the image)
            image = Image.open(io.BytesIO(contents))
            
            # Validate image format matches expected types
            if not image.format or image.format.lower() not in ['png', 'jpeg', 'webp']:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid image format: {image.format or 'unknown'}. Allowed: PNG, JPEG, WEBP"
                )
            
            # Normalize extension based on ACTUAL detected format (not client-supplied)
            # This prevents mismatches between file extension and content
            format_to_ext = {
                'png': '.png',
                'jpeg': '.jpg',  # Canonical: always save as .jpg not .jpeg
                'webp': '.webp'
            }
            
            # Get extension with safe fallback for unknown formats
            detected_format = image.format.lower() if image.format else 'unknown'
            ext = format_to_ext.get(detected_format)
            
            if not ext:
                # Should never happen due to format validation above, but be defensive
                raise HTTPException(
                    status_code=400,
                    detail=f"Unsupported image format after validation: {detected_format}"
                )
            
            # Optionally resize large images to prevent storage issues
            max_dimension = 2048
            if image.width > max_dimension or image.height > max_dimension:
                image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
            
            # Create avatars directory if it doesn't exist
            # Use absolute path to project root, not relative to python_backend
            project_root = Path(__file__).parent.parent
            avatars_dir = project_root / "attached_assets" / "avatars"
            avatars_dir.mkdir(parents=True, exist_ok=True)
            
            # Remove ALL old avatar files regardless of extension
            # Include .jpeg (legacy) even though we now save as .jpg
            for old_ext in [".png", ".jpg", ".jpeg", ".webp"]:
                old_file = avatars_dir / f"{expert_id}{old_ext}"
                if old_file.exists() and old_ext != ext:
                    old_file.unlink()
            
            # Save file with expert_id as filename
            file_path = avatars_dir / f"{expert_id}{ext}"
            
            # Save the validated and potentially resized image
            # This also strips any malicious metadata/payloads
            image.save(file_path, format=image.format, optimize=True)
            
        except Exception as img_error:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid image file: {str(img_error)}"
            )
        
        # Update expert's avatar path
        avatar_url = f"/attached_assets/avatars/{expert_id}{ext}"
        updated_expert = await storage.update_expert_avatar(expert_id, avatar_url)
        
        if not updated_expert:
            raise HTTPException(status_code=500, detail="Failed to update expert avatar")
        
        return updated_expert
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error uploading avatar: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to upload avatar: {str(e)}")
    finally:
        # Ensure file is closed
        await file.close()

# Conversation endpoints
@app.get("/api/conversations", response_model=List[Conversation])
async def get_conversations(expertId: Optional[str] = None):
    """Get conversations, optionally filtered by expert"""
    return await storage.get_conversations(expertId)

@app.get("/api/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str):
    """Get a specific conversation"""
    conversation = await storage.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@app.post("/api/conversations", response_model=Conversation, status_code=201)
async def create_conversation(data: ConversationCreate):
    """Create a new conversation with an expert"""
    try:
        # Verify expert exists
        expert = await storage.get_expert(data.expertId)
        if not expert:
            raise HTTPException(status_code=404, detail="Expert not found")
        
        conversation = await storage.create_conversation(data)
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create conversation: {str(e)}")

# Message endpoints
@app.get("/api/conversations/{conversation_id}/messages", response_model=List[Message])
async def get_messages(conversation_id: str):
    """Get all messages in a conversation"""
    messages = await storage.get_messages(conversation_id)
    return messages

@app.post("/api/conversations/{conversation_id}/messages", response_model=MessageResponse, status_code=201)
async def send_message(conversation_id: str, data: MessageSend):
    """Send a message and get AI response from the marketing legend"""
    try:
        # Validate conversation exists
        conversation = await storage.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Get expert
        expert = await storage.get_expert(conversation.expertId)
        if not expert:
            raise HTTPException(status_code=404, detail="Expert not found")
        
        # Get conversation history BEFORE saving the new user message
        # This way we pass all previous messages to the agent
        all_messages = await storage.get_messages(conversation_id)
        history = [
            {"role": msg.role, "content": msg.content}
            for msg in all_messages
        ]
        
        # Create agent for this expert
        agent = LegendAgentFactory.create_agent(
            expert_name=expert.name,
            system_prompt=expert.systemPrompt
        )
        
        # Get AI response (agent.chat will add the new user message to history)
        ai_response = await agent.chat(history, data.content)
        
        # Now save user message AFTER getting AI response
        user_message = await storage.create_message(MessageCreate(
            conversationId=conversation_id,
            role="user",
            content=data.content
        ))
        
        # Save assistant message
        assistant_message = await storage.create_message(MessageCreate(
            conversationId=conversation_id,
            role="assistant",
            content=ai_response
        ))
        
        return MessageResponse(
            userMessage=user_message,
            assistantMessage=assistant_message
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

# Business Profile endpoints
@app.post("/api/profile", response_model=BusinessProfile)
async def save_profile(data: BusinessProfileCreate):
    """Create or update business profile"""
    # For now, use a default user_id until we add authentication
    user_id = "default_user"
    try:
        profile = await storage.save_business_profile(user_id, data)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save profile: {str(e)}")

@app.get("/api/profile", response_model=Optional[BusinessProfile])
async def get_profile():
    """Get current user's business profile"""
    # For now, use a default user_id until we add authentication
    user_id = "default_user"
    profile = await storage.get_business_profile(user_id)
    return profile

# Council Analysis endpoints
@app.post("/api/council/analyze", response_model=CouncilAnalysis)
async def create_council_analysis(data: CouncilAnalysisCreate):
    """
    Run collaborative analysis by council of marketing legend experts.
    
    This endpoint:
    1. Conducts Perplexity research (if user has BusinessProfile)
    2. Gets independent analyses from 8 marketing legends
    3. Synthesizes consensus recommendation
    """
    # For now, use a default user_id until we add authentication
    user_id = "default_user"
    
    try:
        # Get user's business profile (optional)
        profile = await storage.get_business_profile(user_id)
        
        # Get experts to consult (all 8 if not specified)
        if data.expertIds:
            experts = []
            for expert_id in data.expertIds:
                expert = await storage.get_expert(expert_id)
                if not expert:
                    raise HTTPException(status_code=404, detail=f"Expert {expert_id} not found")
                experts.append(expert)
        else:
            # Use all available experts
            experts = await storage.get_experts()
            if not experts:
                raise HTTPException(status_code=400, detail="No experts available for analysis")
        
        # Run council analysis
        analysis = await council_orchestrator.analyze(
            problem=data.problem,
            experts=experts,
            profile=profile,
            user_id=user_id
        )
        
        # Save analysis
        await storage.save_council_analysis(analysis)
        
        return analysis
    
    except HTTPException:
        raise
    except ValueError as e:
        # Missing API keys (ANTHROPIC_API_KEY, PERPLEXITY_API_KEY)
        error_msg = str(e)
        if "API_KEY" in error_msg or "api_key" in error_msg.lower():
            raise HTTPException(
                status_code=503,
                detail=f"Service temporarily unavailable: {error_msg}"
            )
        raise
    except Exception as e:
        print(f"Error creating council analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Failed to create council analysis: {str(e)}")

@app.post("/api/council/analyze-stream")
async def create_council_analysis_stream(data: CouncilAnalysisCreate):
    """
    Run collaborative analysis with Server-Sent Events streaming.
    
    Emits real-time progress events:
    - expert_started: When expert begins analysis
    - expert_researching: During Perplexity research
    - expert_analyzing: During Claude analysis
    - expert_completed: When expert finishes
    - consensus_started: Before synthesis
    - analysis_complete: Final result with full analysis
    """
    user_id = "default_user"
    
    async def event_generator():
        # Helper to format SSE events (defined outside try block for exception handling)
        def sse_event(event_type: str, data: dict) -> str:
            return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"
        
        try:
            # Get user's business profile (optional)
            profile = await storage.get_business_profile(user_id)
            
            # Get experts to consult
            if data.expertIds:
                experts = []
                for expert_id in data.expertIds:
                    expert = await storage.get_expert(expert_id)
                    if not expert:
                        yield sse_event("error", {"message": f"Expert {expert_id} not found"})
                        return
                    experts.append(expert)
            else:
                experts = await storage.get_experts()
                if not experts:
                    yield sse_event("error", {"message": "No experts available"})
                    return
            
            # Emit initial event with expert list
            yield sse_event("analysis_started", {
                "expertCount": len(experts),
                "experts": [{"id": e.id, "name": e.name, "avatar": e.avatar} for e in experts]
            })
            
            # Run council analysis with progress events
            # We'll need to modify council_orchestrator to emit events
            # For now, we'll simulate the workflow
            
            contributions = []
            research_findings = None
            
            # Perplexity research phase
            if profile:
                yield sse_event("research_started", {
                    "message": "Conducting market research..."
                })
                
                from perplexity_research import PerplexityResearch
                perplexity = PerplexityResearch()
                try:
                    research_result = await perplexity.research(
                        problem=data.problem,
                        profile=profile
                    )
                    research_findings = research_result.get("findings", "")
                    
                    yield sse_event("research_completed", {
                        "message": "Market research complete",
                        "citations": len(research_result.get("sources", []))
                    })
                except Exception as e:
                    yield sse_event("research_failed", {
                        "message": f"Research failed: {str(e)}"
                    })
            
            # Analyze with each expert (emitting events for each)
            from crew_council import council_orchestrator
            
            # Process experts sequentially for event emission
            for expert in experts:
                yield sse_event("expert_started", {
                    "expertId": expert.id,
                    "expertName": expert.name,
                    "message": f"{expert.name} is analyzing..."
                })
                
                try:
                    contribution = await council_orchestrator._get_expert_analysis(
                        expert=expert,
                        problem=data.problem,
                        profile=profile,
                        research_findings=research_findings
                    )
                    contributions.append(contribution)
                    
                    yield sse_event("expert_completed", {
                        "expertId": expert.id,
                        "expertName": expert.name,
                        "insightCount": len(contribution.keyInsights),
                        "recommendationCount": len(contribution.recommendations)
                    })
                except Exception as e:
                    yield sse_event("expert_failed", {
                        "expertId": expert.id,
                        "expertName": expert.name,
                        "error": str(e)
                    })
            
            if not contributions:
                yield sse_event("error", {"message": "All expert analyses failed"})
                return
            
            # Synthesize consensus
            yield sse_event("consensus_started", {
                "message": "Synthesizing council consensus..."
            })
            
            consensus = await council_orchestrator._synthesize_consensus(
                problem=data.problem,
                contributions=contributions,
                research_findings=research_findings
            )
            
            # Create final analysis object
            from models import CouncilAnalysis, AgentContribution
            import uuid
            
            analysis = CouncilAnalysis(
                id=str(uuid.uuid4()),
                userId=user_id,
                problem=data.problem,
                profileId=profile.id if profile else None,
                marketResearch=research_findings,
                contributions=contributions,
                consensus=consensus
            )
            
            # Save analysis
            await storage.save_council_analysis(analysis)
            
            # Send final complete event
            yield sse_event("analysis_complete", {
                "analysisId": analysis.id,
                "analysis": {
                    "id": analysis.id,
                    "problem": analysis.problem,
                    "contributions": [
                        {
                            "expertId": c.expertId,
                            "expertName": c.expertName,
                            "analysis": c.analysis,
                            "keyInsights": c.keyInsights,
                            "recommendations": c.recommendations
                        }
                        for c in analysis.contributions
                    ],
                    "consensus": analysis.consensus
                }
            })
            
        except Exception as e:
            yield sse_event("error", {
                "message": f"Analysis failed: {str(e)}"
            })
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )

@app.get("/api/council/analyses", response_model=List[CouncilAnalysis])
async def get_council_analyses():
    """Get all council analyses for the current user"""
    # For now, use a default user_id until we add authentication
    user_id = "default_user"
    return await storage.get_council_analyses(user_id)

@app.get("/api/council/analyses/{analysis_id}", response_model=CouncilAnalysis)
async def get_council_analysis(analysis_id: str):
    """Get a specific council analysis by ID"""
    analysis = await storage.get_council_analysis(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Council analysis not found")
    return analysis

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
