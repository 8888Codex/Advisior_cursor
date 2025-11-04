"""
Clone Registry - Sistema de descoberta e registro de clones
Permite auto-discovery e fallback para prompts
"""
from typing import Dict, Type, Optional
import importlib
import os


class CloneRegistry:
    """
    Registry central para todos os clones de especialistas
    
    Permite:
    - Auto-discovery de clones disponíveis
    - Fallback gracioso para prompts se clone não existir
    - Versionamento e migração gradual
    """
    
    _clones: Dict[str, Type] = {}
    _initialized = False
    
    @classmethod
    def register(cls, expert_name: str, clone_class: Type):
        """
        Registra um clone
        
        Args:
            expert_name: Nome do especialista (ex: "Philip Kotler")
            clone_class: Classe do clone
        """
        cls._clones[expert_name] = clone_class
        print(f"[CloneRegistry] ✅ Registrado: {expert_name}")
    
    @classmethod
    def get_clone(cls, expert_name: str) -> Optional[Type]:
        """
        Busca clone por nome
        
        Args:
            expert_name: Nome do especialista
            
        Returns:
            Classe do clone ou None se não existir
        """
        cls._ensure_initialized()
        return cls._clones.get(expert_name)
    
    @classmethod
    def has_clone(cls, expert_name: str) -> bool:
        """Verifica se clone está disponível"""
        cls._ensure_initialized()
        return expert_name in cls._clones
    
    @classmethod
    def list_available_clones(cls) -> list:
        """Lista todos os clones disponíveis"""
        cls._ensure_initialized()
        return list(cls._clones.keys())
    
    @classmethod
    def _ensure_initialized(cls):
        """Inicializa registry se ainda não foi feito"""
        if cls._initialized:
            return
        
        cls._auto_discover_clones()
        cls._initialized = True
    
    @classmethod
    def _auto_discover_clones(cls):
        """
        Auto-descobre todos os clones disponíveis no diretório clones/ E clones/custom/
        
        Procura por arquivos *_clone.py e tenta importar automaticamente
        """
        try:
            clones_dir = os.path.dirname(__file__)
            
            # 1. Descobrir clones pré-prontos (diretório principal)
            for filename in os.listdir(clones_dir):
                if filename.endswith('_clone.py'):
                    module_name = filename[:-3]  # Remove .py
                    
                    try:
                        # Import module dinamicamente
                        module = importlib.import_module(f'python_backend.clones.{module_name}')
                        
                        # Procurar por classe que herda de ExpertCloneBase
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            
                            # Check if it's a class and subclass of ExpertCloneBase
                            if (isinstance(attr, type) and 
                                hasattr(attr, '__mro__') and 
                                'ExpertCloneBase' in [c.__name__ for c in attr.__mro__]):
                                
                                # Instanciar para pegar o nome
                                try:
                                    instance = attr()
                                    expert_name = instance.name
                                    cls.register(expert_name, attr)
                                except:
                                    # Se não conseguir instanciar, skip
                                    pass
                    
                    except ImportError as e:
                        # Clone não pode ser importado - skip silenciosamente
                        # (Permite migração gradual)
                        pass
                    except Exception as e:
                        print(f"[CloneRegistry] Warning: Erro ao importar {module_name}: {e}")
            
            # 2. 🆕 Descobrir clones customizados (diretório custom/)
            custom_dir = os.path.join(clones_dir, 'custom')
            if os.path.exists(custom_dir):
                cls._discover_custom_clones(custom_dir)
        
        except Exception as e:
            print(f"[CloneRegistry] Warning: Erro no auto-discovery: {e}")
    
    @classmethod
    def _discover_custom_clones(cls, custom_dir: str):
        """
        Descobre clones customizados no diretório custom/
        
        Args:
            custom_dir: Caminho para o diretório custom/
        """
        try:
            for filename in os.listdir(custom_dir):
                if not filename.endswith('_clone.py') or filename == '__init__.py':
                    continue
                
                module_name = filename[:-3]  # Remove .py
                
                try:
                    # Import module dinamicamente
                    module = importlib.import_module(f'python_backend.clones.custom.{module_name}')
                    
                    # Procurar por classe que herda de ExpertCloneBase
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        
                        # Check if it's a class and subclass of ExpertCloneBase
                        if (isinstance(attr, type) and 
                            hasattr(attr, '__mro__') and 
                            'ExpertCloneBase' in [c.__name__ for c in attr.__mro__]):
                            
                            # Instanciar para pegar o nome
                            try:
                                instance = attr()
                                expert_name = instance.name
                                cls.register(expert_name, attr)
                                print(f"[CloneRegistry] ✅ Clone customizado carregado: {expert_name}")
                            except:
                                pass
                
                except Exception as e:
                    print(f"[CloneRegistry] ⚠️ Erro ao carregar custom clone {module_name}: {e}")
        
        except Exception as e:
            print(f"[CloneRegistry] Warning: Erro ao descobrir custom clones: {e}")
    
    @classmethod
    def get_coverage_stats(cls) -> Dict[str, int]:
        """
        Retorna estatísticas de cobertura de clones
        
        Returns:
            Dict com total de clones e porcentagem vs. prompts
        """
        cls._ensure_initialized()
        
        return {
            "total_clones": len(cls._clones),
            "available_clones": list(cls._clones.keys()),
            "coverage_percent": (len(cls._clones) / 18) * 100  # 18 = total de especialistas
        }


# ============================================================================
# FUNÇÕES HELPER
# ============================================================================

def get_clone_or_none(expert_name: str):
    """
    Busca clone por nome, retorna None se não existir
    
    Usage:
        clone = get_clone_or_none("Philip Kotler")
        if clone:
            response = clone().process_input("...")
        else:
            # Fallback para prompt
            use_prompt_based_approach()
    """
    return CloneRegistry.get_clone(expert_name)


def is_clone_available(expert_name: str) -> bool:
    """Verifica se especialista tem clone Python disponível"""
    return CloneRegistry.has_clone(expert_name)

