import { Link, useLocation } from "wouter";
import { ReactNode } from "react";
import { cn } from "@/lib/utils";
import { 
  Home, 
  Users, 
  Tag, 
  MessageSquare, 
  Sparkles, 
  UserPlus,
  UsersRound,
  FileText
} from "lucide-react";

interface SidebarItem {
  href: string;
  label: string;
  icon: ReactNode;
  testId?: string;
}

const sidebarItems: SidebarItem[] = [
  { href: "/home", label: "Home", icon: <Home className="h-4 w-4" />, testId: "sidebar-home" },
  { href: "/experts", label: "Especialistas", icon: <Users className="h-4 w-4" />, testId: "sidebar-experts" },
  { href: "/categories", label: "Categorias", icon: <Tag className="h-4 w-4" />, testId: "sidebar-categories" },
  { href: "/test-council", label: "Conselho Estratégico", icon: <UsersRound className="h-4 w-4" />, testId: "sidebar-council" },
  { href: "/personas", label: "Persona Builder", icon: <FileText className="h-4 w-4" />, testId: "sidebar-personas" },
  { href: "/create", label: "Criar Especialista", icon: <UserPlus className="h-4 w-4" />, testId: "sidebar-create" },
];

interface SidebarProps {
  className?: string;
}

/**
 * Sidebar component - Navegação lateral reutilizável
 * Usa wouter para highlight da rota ativa
 */
export function Sidebar({ className }: SidebarProps) {
  const [location] = useLocation();

  return (
    <aside className={cn("w-64 border-r bg-background p-4", className)}>
      <nav className="space-y-1">
        {sidebarItems.map((item) => {
          const isActive = location === item.href || 
            (item.href !== "/home" && location.startsWith(item.href));
          
          return (
            <Link key={item.href} href={item.href}>
              <div
                className={cn(
                  "flex items-center gap-3 px-3 py-2 rounded-lg transition-colors cursor-pointer",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                )}
                data-testid={item.testId}
              >
                {item.icon}
                <span className="text-sm font-medium">{item.label}</span>
              </div>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}

