/**
 * Validações Centralizadas
 * Single source of truth para todas as regras de validação
 */

import { ValidationError } from "./errors";
import type { CouncilAnalysisRequest } from "@/types/council";

/**
 * Validações para análise do conselho
 */
export const CouncilValidation = {
  /**
   * Valida problema/questão do usuário
   */
  problem: {
    minLength: 10,
    maxLength: 5000,
    
    validate(problem: string): string | null {
      const trimmed = problem.trim();
      
      if (!trimmed) {
        return "O problema não pode estar vazio";
      }
      
      if (trimmed.length < this.minLength) {
        return `O problema deve ter pelo menos ${this.minLength} caracteres (atual: ${trimmed.length})`;
      }
      
      if (trimmed.length > this.maxLength) {
        return `O problema não pode ter mais de ${this.maxLength} caracteres`;
      }
      
      return null; // válido
    },
    
    isValid(problem: string): boolean {
      return this.validate(problem) === null;
    }
  },

  /**
   * Valida seleção de especialistas
   */
  experts: {
    minCount: 1,
    maxCount: 10,
    
    validate(expertIds: string[]): string | null {
      if (!expertIds || expertIds.length === 0) {
        return "Selecione pelo menos um especialista";
      }
      
      if (expertIds.length < this.minCount) {
        return `Selecione pelo menos ${this.minCount} especialista${this.minCount > 1 ? 's' : ''}`;
      }
      
      if (expertIds.length > this.maxCount) {
        return `Selecione no máximo ${this.maxCount} especialistas`;
      }
      
      return null; // válido
    },
    
    isValid(expertIds: string[]): boolean {
      return this.validate(expertIds) === null;
    }
  },

  /**
   * Valida persona
   */
  persona: {
    validate(personaId: string | undefined): string | null {
      if (!personaId || !personaId.trim()) {
        return "Você precisa selecionar uma persona antes de usar o conselho";
      }
      
      return null; // válido
    },
    
    isValid(personaId: string | undefined): boolean {
      return this.validate(personaId) === null;
    }
  },

  /**
   * Valida request completo de análise
   */
  request: {
    validate(request: Partial<CouncilAnalysisRequest>): {
      isValid: boolean;
      errors: Record<string, string>;
      firstError?: string;
    } {
      const errors: Record<string, string> = {};

      const problemError = CouncilValidation.problem.validate(request.problem || "");
      if (problemError) errors.problem = problemError;

      const expertsError = CouncilValidation.experts.validate(request.expertIds || []);
      if (expertsError) errors.experts = expertsError;

      const personaError = CouncilValidation.persona.validate(request.personaId);
      if (personaError) errors.persona = personaError;

      const isValid = Object.keys(errors).length === 0;
      const firstError = Object.values(errors)[0];

      return { isValid, errors, firstError };
    },
    
    validateOrThrow(request: Partial<CouncilAnalysisRequest>): void {
      const result = this.validate(request);
      
      if (!result.isValid) {
        const firstKey = Object.keys(result.errors)[0];
        throw new ValidationError(result.firstError!, firstKey);
      }
    }
  }
};

/**
 * Helper para validar e mostrar erro no toast
 */
export function validateCouncilRequest(
  request: Partial<CouncilAnalysisRequest>,
  toast: (props: any) => void
): boolean {
  const validation = CouncilValidation.request.validate(request);
  
  if (!validation.isValid) {
    toast({
      variant: "destructive",
      title: "Validação falhou",
      description: validation.firstError,
      duration: 5000,
    });
    return false;
  }
  
  return true;
}

