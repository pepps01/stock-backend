export default function BlogLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return <section className="bg-amber-600 p-8 m-2.5">{children}</section>
}