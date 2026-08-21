interface ServiceDetailPageProps {
  id: string
}

export default function ServiceDetailPage({ id }: ServiceDetailPageProps) {
  return (
    <div>
      <h2 style={{ marginBottom: '1rem' }}>Service: {id}</h2>
      {/* TODO: Implement if needed */}
      <p style={{ color: '#666' }}>Service detail page — implement me!</p>
    </div>
  )
}
