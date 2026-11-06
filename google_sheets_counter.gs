
const SECRET = "change-me-to-a-long-random-word";   

function doPost(e) {
  const d = JSON.parse(e.postData.contents);
  SpreadsheetApp.getActiveSpreadsheet().getActiveSheet()
    .appendRow([d.ts, d.session, d.event, d.fields, d.dream, d.top]);
  return ContentService.createTextOutput("ok");
}

function doGet(e) {                                  
  if (!e.parameter || e.parameter.key !== SECRET)
    return ContentService.createTextOutput("[]").setMimeType(ContentService.MimeType.JSON);
  const rows = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet().getDataRange().getValues();
  return ContentService.createTextOutput(JSON.stringify(rows)).setMimeType(ContentService.MimeType.JSON);
}
