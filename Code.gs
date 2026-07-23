const QUESTIONS_SHEET = "Sheet1";
const SCORES_SHEET = "Scores";

function doGet() {
  return HtmlService.createHtmlOutputFromFile("Index")
    .setTitle("Candidate Interview Scoring");
}

function getFinalQuestions() {

  const sh = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Sheet1");

  const data = sh.getRange(2,1,sh.getLastRow()-1,3).getValues();

  const questions = [];

  data.forEach(function(row){

    if(row[2] === true){

      questions.push({
        category: row[0],
        question: row[1]
      });

    }

  });

  return questions;

}

function submitScores(payload) {

  const ss = SpreadsheetApp.getActiveSpreadsheet();

  let sh = ss.getSheetByName(SCORES_SHEET);

  if (!sh) {

    sh = ss.insertSheet(SCORES_SHEET);

    sh.appendRow([
      "Timestamp",
      "Candidate Name",
      "Category",
      "Question",
      "Score",
      "Notes"
    ]);

  }

  const timestamp = new Date();

  let total = 0;

  payload.answers.forEach(function(ans){

    total += Number(ans.score);

    sh.appendRow([
      timestamp,
      payload.candidateName,
      ans.category,
      ans.question,
      ans.score,
      ans.notes
    ]);

  });

  sh.appendRow([
    "",
    payload.candidateName,
    "",
    "TOTAL",
    total,
    ""
  ]);

  return {
    success:true,
    total:total
  };

}