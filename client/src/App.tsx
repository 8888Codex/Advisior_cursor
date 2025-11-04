import { Switch, Route, useLocation } from "wouter";
import { useEffect } from "react";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { ThemeProvider } from "@/components/ThemeProvider";
import { Header } from "@/components/Header";
import { ErrorBanner } from "@/components/ErrorBanner";
import { GlobalErrorProvider, useGlobalError } from "@/hooks/useGlobalError";
import { AnimatePresence } from "framer-motion";
import NotFound from "@/pages/not-found";
import Landing from "@/pages/Landing";
import Home from "@/pages/Home";
import Experts from "@/pages/Experts";
import Categories from "@/pages/Categories";
import Chat from "@/pages/Chat";
import Create from "@/pages/Create";
import AdminExperts from "@/pages/AdminExperts";
import Onboarding from "@/pages/Onboarding";
import TestCouncil from "@/pages/TestCouncil";
import Personas from "@/pages/Personas";
import FeaturesAnalysis from "@/pages/FeaturesAnalysis";
import CouncilChat from "@/pages/CouncilChat";

function Redirect({ to }: { to: string }) {
  const [, setLocation] = useLocation();
  
  // Use useEffect para evitar setState durante render
  useEffect(() => {
    setLocation(to);
  }, [to, setLocation]);
  
  return null;
}

function Router() {
  const [location] = useLocation();
  
  return (
    <AnimatePresence mode="wait">
      <Switch location={location} key={location}>
        <Route path="/" component={Landing} />
        <Route path="/home" component={Home} />
        <Route path="/welcome">
          <Redirect to="/" />
        </Route>
        <Route path="/marketing">
          <Redirect to="/" />
        </Route>
        <Route path="/onboarding" component={Onboarding} />
        <Route path="/experts" component={Experts} />
        <Route path="/categories" component={Categories} />
        <Route path="/chat/:id" component={Chat} />
        <Route path="/create" component={Create} />
        <Route path="/admin/experts" component={AdminExperts} />
        <Route path="/test-council" component={TestCouncil} />
        <Route path="/council-chat/:id" component={CouncilChat} />
        <Route path="/personas" component={Personas} />
        <Route path="/features" component={FeaturesAnalysis} />
        <Route component={NotFound} />
      </Switch>
    </AnimatePresence>
  );
}

function AppContent() {
  const { error, clearError } = useGlobalError();

  return (
    <>
      {error && (
        <div className="container mx-auto px-4 pt-4">
          <ErrorBanner
            title={error.title}
            message={error.message}
            onRetry={error.onRetry}
            retryLabel={error.retryLabel}
            onDismiss={clearError}
          />
        </div>
      )}
      <div className="min-h-screen bg-background text-foreground">
        <Header />
        <Router />
      </div>
    </>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <TooltipProvider>
          <GlobalErrorProvider>
            <AppContent />
            <Toaster />
          </GlobalErrorProvider>
        </TooltipProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;
