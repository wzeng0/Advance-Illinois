
import './App.css';
import { useState } from "react";
import { pdfjs, Document, Page } from "react-pdf";

pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/legacy/build/pdf.worker.min.js`;

export default function App() {
  const [metadata, setMetadata] = useState();

  async function onLoadSuccess(pdf) {
    setMetadata(await pdf.getMetadata());
  }

  return (
    <Document file="sample.pdf" onLoadSuccess={onLoadSuccess}>
      <Page pageNumber={2} />
      <h2>Metadata</h2>
      <pre>{JSON.stringify(metadata, null, 2)}</pre>
    </Document>
  );
}