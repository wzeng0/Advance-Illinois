import * as XLSX from 'xlsx';

// eslint-disable-next-line no-restricted-globals
self.addEventListener('message', (event) => {
  const file = event.data;

  const reader = new FileReader();
  reader.onload = (event) => {
    const binaryString = event.target.result;
    const workBook = XLSX.read(binaryString, { type: 'binary' });

    const sheetName = "House";
    const sheet = workBook.Sheets[sheetName];

    const columnNames = XLSX.utils.sheet_to_json(sheet, { header: 1 })[0];

    // Send the extracted column names back to the main thread
    // eslint-disable-next-line no-restricted-globals
    self.postMessage(columnNames);
  };

  reader.readAsBinaryString(file);
});
