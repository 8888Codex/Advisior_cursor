import { Switch, Route } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { ThemeProvider } from "@/components/ThemeProvider";
import { Header } from "@/components/Header";
import NotFound from "@/pages/not-found";
import Home from "@/pages/Home";
import Experts from "@/pages/Experts";
import Chat from "@/pages/Chat";
import Create from "@/pages/Create";
import AdminExperts from "@/pages/AdminExperts";
import Onboarding from "@/pages/Onboarding";
import TestCouncil from "@/pages/TestCouncil";

function Router() {
  return (
    <Switch>
      <Route path="/" component={Home} />
      <Route path="/onboarding" component={Onboarding} />
      <Route path="/experts" component={Experts} />
      <Route path="/chat/:id" component={Chat} />
      <Route path="/create" component={Create} />
      <Route path="/admin/experts" component={AdminExperts} />
      <Route path="/test-council" component={TestCouncil} />
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <TooltipProvider>
          <div className="min-h-screen bg-background text-foreground">
            <Header />
            <Router />
          </div>
          <Toaster />
        </TooltipProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
