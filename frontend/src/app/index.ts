import { redirect } from 'next/navigation';

export default function Home() {
  // If the user visits the root / route, let's redirect them to the landing page or dashboard
  // For now we'll render the Landing Page directly via the previous page.tsx
  // Since we already created src/app/page.tsx with the beautiful landing, this is fine.
  return null;
}
