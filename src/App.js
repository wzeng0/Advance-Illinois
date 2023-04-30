import React from 'react';
import { Document, Page } from 'react-pdf/dist/esm/entry.webpack';
import { saveAs } from 'file-saver';
import axios from 'axios';
import './App.css';

// Replace the URL with the URL of your PDF file
const pdfUrl = 'https://example.com/your_pdf_file.pdf';

function App() {
    const [numPages, setNumPages] = React.useState(null);

    function onDocumentLoadSuccess({ numPages }) {
        setNumPages(numPages);
    }

    const downloadPdf = async() => {
        try {
            const response = await axios.get(pdfUrl, {
                responseType: 'blob',
            });

            const fileName = 'downloaded_file.pdf';
            saveAs(new Blob([response.data], { type: 'application/pdf' }), fileName);
        } catch (error) {
            console.error('Error while downloading PDF:', error);
        }
    };

    return ( <
        div className = "App" >
        <
        header className = "App-header" >
        <
        h1 > PDF Viewer < /h1> <
        button onClick = { downloadPdf } > Download PDF < /button> <
        Document file = { pdfUrl }
        onLoadSuccess = { onDocumentLoadSuccess }
        loading = { < p > Loading PDF... < /p>} >
            {
                Array.from(new Array(numPages), (_, index) => ( <
                    Page key = { `page_${index + 1}` }
                    pageNumber = { index + 1 }
                    />
                ))
            } <
            /Document> <
            /header> <
            /div>
        );
    }

    export default App;