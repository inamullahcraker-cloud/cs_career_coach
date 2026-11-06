// Paste this into Extensions > Apps Script in a NEW Google Sheet. Then Deploy > New deployment >
// Web app > Execute as: Me > Who has access: Anyone. Copy the Web app URL.
const SECRET = "change-me-to-a-long-random-word";   // same value goes in TRACKER_KEY

function doPost(e) {
  const d = JSON.parse(e.postData.contents);
  SpreadsheetApp.getActiveSpreadsheet().getActiveSheet()
    .appendRow([d.ts, d.session, d.event, d.fields, d.dream, d.top]);
  return ContentService.createTextOutput("ok");
}

function doGet(e) {                                  // only the admin page reads, using the secret
  if (!e.parameter || e.parameter.key !== SECRET)
    return ContentService.createTextOutput("[]").setMimeType(ContentService.MimeType.JSON);
  const rows = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet().getDataRange().getValues();
  return ContentService.createTextOutput(JSON.stringify(rows)).setMimeType(ContentService.MimeType.JSON);
}
