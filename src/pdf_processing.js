
import './App.css';
import { useState } from "react";
import { pdfjs, Document, Page } from "react-pdf";
import { usePDF, Document, Page, Text, View, StyleSheet } from '@react-pdf/renderer';

// Not sure what this doesn but it makes getting the PDF happen
// pdfjs.GlobalWorkerOptions.workerSrc = `//unpkg.com/pdfjs-dist@${pdfjs.version}/legacy/build/pdf.worker.min.js`;

// Style Sheet for the new PDF
const styles = StyleSheet.create({
	page: {
		flexDirection: 'row',
	},
	section: {
		flexGrow: 1,
	},
});

// New Document containing the things we need
const MyDocument = (
	<Document>
		<Page size="A4" style={styles.page}>
			<View style={styles.section}>
				<Text>Hello World!</Text>
			</View>
			<View style={styles.section}>
				<Text>We're inside a PDF!</Text>
			</View>
		</Page>
	</Document>
);

export default function App() {
    // Loads the document into a PDF
    const [instance, updateInstance] = usePDF({ document: MyDocument });

    // Processing time
    if (instance.loading) return <div>Loading ...</div>;
    // Catches any errors
    if (instance.error) return <div>Something went wrong: {instance.error}</div>;

    return (
        // A click text that downloads the pdf upon click
        <a href={instance.url} download="test.pdf">
        Download
        </a>
    );

    // Getting the Meta data of the application
    //   const [metadata, setMetadata] = useState();

    // Loading a given PDF
    //   async function onLoadSuccess(pdf) {
    //     setMetadata(await pdf.getMetadata());
    //   }

    //   return (
    //     <Document file="sample.pdf" onLoadSuccess={onLoadSuccess}>
    //       <Page pageNumber={2} />
    //       <h2>Metadata</h2>
    //       <pre>{JSON.stringify(metadata, null, 2)}</pre>
    //     </Document>
    //   );
}