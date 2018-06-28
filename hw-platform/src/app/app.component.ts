import { Component, OnInit } from '@angular/core';

import { CourseService } from "./course.service";
import { Homework } from './homework';
import { HomeworkDetailComponent} from "./homework-detail/homework-detail.component";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  specialisationsByYear: object;
  selectedYear: string;
  selectedSpecialisation: string;
  homeworkList: any;

  // Variables for adding a new homework to the list
  selectedYearForm: string;
  selectedSpecialisationForm: string;
  showAddForm: boolean;
  homeworkListForm: any;
  selectedCourseForm: object;
  courses: object[];

  constructor(private _courseService : CourseService) {}

  ngOnInit() {
    this.specialisationsByYear = this._courseService.getYearsWithSpecialisations();
    this.showAddForm = false;
  }

  updateHomework() {
    if (!this.selectedYear || !this.selectedSpecialisation) {
      return;
    }
    this._courseService.getHomework(this.selectedYear, this.selectedSpecialisation)
      .subscribe((res) => {
        this.homeworkList = res;
      });
  }

  getYears() {
    return Object.keys(this.specialisationsByYear);
  }

  getSpecialisations() {
    if (this.selectedYear) {
      return this.specialisationsByYear[this.selectedYear];
    }
    return null;
  }

  selectYear(year) {
    this.selectedYear = year;
    console.log("Selected year " + year);
  }

  selectSpecialisation(specialisation) {
    this.selectedSpecialisation = specialisation;
    console.log("Selected specialisation " + specialisation);

    this.updateHomework();
  }

  /////////// Methods for adding new homework
  getSpecialisationsForm() {
    if (this.selectedYearForm) {
      return this.specialisationsByYear[this.selectedYearForm];
    }
    return null;
  }

  selectYearForm(year) {
    this.selectedYearForm = year;
    console.log("Selected year " + year);
  }

  selectSpecialisationForm(specialisation) {
    this.selectedSpecialisationForm = specialisation;
    console.log("Selected specialisation " + specialisation);

    this.updateHomeworkForm();
  }

  selectCourseForm(course) {
    this.selectedCourseForm = course;
  }

  updateHomeworkForm() {
    this._courseService.getHomework(this.selectedYearForm, this.selectedSpecialisationForm)
      .subscribe((res) => {
        this.homeworkListForm = res;
        this.updateCoursesForm();
      });
  }

  updateCoursesForm() {
    this.courses = this.homeworkListForm.map((h) => h["courseName"]);
    console.log("courses " + this.courses);
  }

  addNewHomework() {
    let newHomework = this.homeworkListForm.find((h) => h["courseName"] === this.selectedCourseForm);
    if (newHomework) {
      this.homeworkList.push(newHomework);
    }

    this.selectedCourseForm = undefined;
    this.selectedYearForm = undefined;
    this.selectedSpecialisationForm = undefined;
    this.showAddForm = false;
  }
}
