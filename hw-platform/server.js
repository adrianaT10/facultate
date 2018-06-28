const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const http = require('http');
const mysql = require('mysql');
const app = express();

if (!process.argv[2]) {
  return;
}

var connection = mysql.createConnection({
  host     : process.argv[2],
  port     : '3306',
  user     : 'homework',
  password : 'homework',
  database : 'homework'
});

// Parsers
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false}));

// Angular DIST output folder
app.use(express.static(path.join(__dirname, 'dist')));

app.get('/get-homework', (req, res) => {
	console.log(req.query);
	var year = req.query.year;
	var specialisation = req.query.specialisation;
	//to add: doar temele care urmeaza!

	connection.query('SELECT c.HOMEWORK_NAME, c.DEADLINE_HARD, c.DEADLINE_SOFT, b.COURSE_NAME' +
                    ' FROM homework.HOMEWORKS c, homework.COURSES b' +
					' WHERE c.CourseID=b.CourseID AND b.CourseID IN ' + 
					'(SELECT CourseID FROM homework.YEAR_COURSES WHERE YEAR=' + 
					year + ' AND SPECIALISATION=\'' + specialisation + '\')', function (err, rows, fields) {
	    if (err) throw err;

	    console.log('The solution is: ', rows);

	    rows = rows.map((h) =>  {return {
	        'homeworkName': h["HOMEWORK_NAME"],
            'courseName': h["COURSE_NAME"],
            'deadlineHard': h["DEADLINE_HARD"],
            'deadlineSoft': h["DEADLINE_SOFT"]
        }});

        res.send(rows);
	});
});

// Send all other requests to the Angular app
app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, 'dist/index.html'));
});

//Set Port
const port = process.env.PORT || '3000';
app.set('port', port);

const server = http.createServer(app);

server.listen(port, () => console.log(`Running on localhost:${port}`));
