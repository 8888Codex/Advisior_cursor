import { Card } from "@/components/ui/card";
import { motion } from "framer-motion";

interface SkeletonCardProps {
  className?: string;
}

export function SkeletonCard({ className = "" }: SkeletonCardProps) {
  return (
    <Card className={`p-8 gap-6 rounded-3xl ${className}`}>
      <div className="flex items-start gap-4">
        {/* Avatar Skeleton */}
        <motion.div
          className="h-24 w-24 rounded-full bg-muted shimmer"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3 }}
        />

        <div className="flex-1 space-y-3">
          {/* Name Skeleton */}
          <motion.div
            className="h-6 w-3/4 bg-muted rounded-xl shimmer"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          />
          {/* Title Skeleton */}
          <motion.div
            className="h-4 w-1/2 bg-muted rounded-xl shimmer"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3, delay: 0.2 }}
          />
        </div>
      </div>

      {/* Expertise Badges Skeleton */}
      <div className="flex flex-wrap gap-2 mt-4">
        {[1, 2, 3].map((i) => (
          <motion.div
            key={i}
            className="h-6 w-24 bg-muted rounded-full shimmer"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3, delay: 0.1 * i + 0.3 }}
          />
        ))}
      </div>

      {/* Bio Skeleton */}
      <div className="space-y-2 mt-4">
        <motion.div
          className="h-4 w-full bg-muted rounded-xl shimmer"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.6 }}
        />
        <motion.div
          className="h-4 w-5/6 bg-muted rounded-xl shimmer"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.3, delay: 0.7 }}
        />
      </div>

      {/* Button Skeleton */}
      <motion.div
        className="h-10 w-full bg-muted rounded-xl shimmer mt-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3, delay: 0.8 }}
      />
    </Card>
  );
}

export function ExpertGridSkeleton({ count = 6 }: { count?: number }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      {Array.from({ length: count }).map((_, i) => (
        <motion.div
          key={i}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{
            duration: 0.4,
            delay: i * 0.1,
            ease: [0.4, 0, 0.2, 1],
          }}
        >
          <SkeletonCard />
        </motion.div>
      ))}
    </div>
  );
}
