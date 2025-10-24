import { useState, useEffect } from "react";
import { useLocation } from "wouter";

/**
 * Custom hook that syncs with URL search parameters
 * Observes window.location.search changes via multiple mechanisms:
 * - popstate events (browser back/forward)
 * - wouter location changes (programmatic navigation)
 * - Direct window.location reads (ensures accuracy)
 * 
 * This hook provides reliable URL search param access regardless of how navigation occurs.
 */
export function useURLSearchParams(): URLSearchParams {
  const [location] = useLocation();
  const [searchParams, setSearchParams] = useState<URLSearchParams>(
    () => new URLSearchParams(window.location.search)
  );

  useEffect(() => {
    // Function to sync search params from current URL
    const syncFromURL = () => {
      const currentParams = new URLSearchParams(window.location.search);
      // Only update if actually different to avoid infinite loops
      const currentString = currentParams.toString();
      const stateString = searchParams.toString();
      if (currentString !== stateString) {
        setSearchParams(currentParams);
      }
    };

    // Sync immediately when effect runs
    syncFromURL();

    // Listen for browser back/forward navigation
    const handlePopState = () => {
      syncFromURL();
    };

    // Listen for any URL changes (catches all navigation types)
    const handleLocationChange = () => {
      syncFromURL();
    };

    window.addEventListener("popstate", handlePopState);
    window.addEventListener("hashchange", handleLocationChange);

    // FALLBACK: Poll for URL changes every 100ms
    // This catches programmatic navigation that doesn't trigger events
    const pollInterval = setInterval(() => {
      syncFromURL();
    }, 100);

    // Cleanup
    return () => {
      window.removeEventListener("popstate", handlePopState);
      window.removeEventListener("hashchange", handleLocationChange);
      clearInterval(pollInterval);
    };
  }, [location, searchParams]); // Re-sync whenever wouter location OR searchParams changes

  return searchParams;
}

/**
 * Helper hook to get a specific URL search parameter value
 */
export function useURLSearchParam(key: string, defaultValue: string = ""): string {
  const searchParams = useURLSearchParams();
  return searchParams.get(key) || defaultValue;
}
