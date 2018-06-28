webpackJsonp(["main"],{

/***/ "../../../../../src/$$_lazy_route_resource lazy recursive":
/***/ (function(module, exports) {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncatched exception popping up in devtools
	return Promise.resolve().then(function() {
		throw new Error("Cannot find module '" + req + "'.");
	});
}
webpackEmptyAsyncContext.keys = function() { return []; };
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
module.exports = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = "../../../../../src/$$_lazy_route_resource lazy recursive";

/***/ }),

/***/ "../../../../../src/app/app.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".addBtn {\n}\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/app.component.html":
/***/ (function(module, exports) {

module.exports = "<nav class=\"navbar navbar-dark bg-dark\">\n  <a href=\"#\" class=\"navbar-brand\">Homework Viewer</a>\n</nav>\n\n<!-- First 2 dropdowns-->\n<div class=\"container my-2\">\n  <div class=\"row justify-content-md-center\">\n\n    <div class=\"col-md-auto\">\n      <div class=\"dropdown\">\n        <button class=\"btn btn-danger dropdown-toggle\" type=\"button\" id=\"dropdownMenuButton\" data-toggle=\"dropdown\"\n                aria-haspopup=\"true\" aria-expanded=\"false\">\n          {{selectedYear || \"Year\"}}\n        </button>\n        <div class=\"dropdown-menu\" aria-labelledby=\"dropdownMenuButton\">\n          <a class=\"dropdown-item\" href=\"#\" *ngFor=\"let year of getYears()\" (click)=\"selectYear(year)\">{{year}}</a>\n        </div>\n      </div>\n    </div>\n\n    <div class=\"col-md-auto\">\n      <div class=\"dropdown\">\n        <button class=\"btn btn-danger dropdown-toggle\" type=\"button\" id=\"dropdownMenuButton\" data-toggle=\"dropdown\"\n                aria-haspopup=\"true\" aria-expanded=\"false\">\n          {{selectedSpecialisation || \"Specialisation\"}}\n        </button>\n        <div class=\"dropdown-menu\" aria-labelledby=\"dropdownMenuButton\">\n          <a class=\"dropdown-item\" href=\"#\" *ngFor=\"let specialisation of getSpecialisations()\"\n             (click)=\"selectSpecialisation(specialisation)\">{{specialisation}}</a>\n        </div>\n      </div>\n    </div>\n\n  </div>\n</div>\n\n<!-- Homework list -->\n<div *ngIf=\"homeworkList\">\n  <div class=\"list-group my-3\">\n    <homework-detail *ngFor=\"let h of homeworkList\" [homework]=\"h\" ></homework-detail>\n  </div>\n\n  <div class=\"d-flex justify-content-center mt-2\">\n    <button (click)=\"showAddForm=true\" class=\"btn btn-outline-dark justify-content-center\">+</button>\n  </div>\n\n\n  <!-- Add new homework form -->\n  <div *ngIf=\"showAddForm\">\n    <div class=\"container my-2\">\n\n      <!-- Dropdowns -->\n      <div class=\"row justify-content-center\">\n\n        <div class=\"col-md-auto\">\n          <div class=\"dropdown\">\n            <button class=\"btn btn-info dropdown-toggle\" type=\"button\" id=\"dropdownMenuButton\" data-toggle=\"dropdown\"\n                    aria-haspopup=\"true\" aria-expanded=\"false\">\n              {{selectedYearForm || \"Year\"}}\n            </button>\n            <div class=\"dropdown-menu\" aria-labelledby=\"dropdownMenuButton\">\n              <a class=\"dropdown-item\" href=\"#\" *ngFor=\"let year of getYears()\" (click)=\"selectYearForm(year)\">{{year}}</a>\n            </div>\n          </div>\n        </div>\n\n        <div class=\"col-md-auto\">\n          <div class=\"dropdown\">\n            <button class=\"btn btn-info dropdown-toggle\" type=\"button\" id=\"dropdownMenuButton\" data-toggle=\"dropdown\"\n                    aria-haspopup=\"true\" aria-expanded=\"false\">\n              {{selectedSpecialisationForm || \"Specialisation\"}}\n            </button>\n            <div class=\"dropdown-menu\" aria-labelledby=\"dropdownMenuButton\">\n              <a class=\"dropdown-item\" href=\"#\" *ngFor=\"let specialisation of getSpecialisationsForm()\"\n                 (click)=\"selectSpecialisationForm(specialisation)\">{{specialisation}}</a>\n            </div>\n          </div>\n        </div>\n\n        <div class=\"col-md-auto\">\n          <div class=\"dropdown\">\n            <button class=\"btn btn-info dropdown-toggle\" type=\"button\" id=\"dropdownMenuButton\" data-toggle=\"dropdown\"\n                    aria-haspopup=\"true\" aria-expanded=\"false\">\n              {{selectedCourseForm || \"Course\"}}\n            </button>\n            <div class=\"dropdown-menu\" aria-labelledby=\"dropdownMenuButton\">\n              <a class=\"dropdown-item\" href=\"#\" *ngFor=\"let course of courses\"\n                 (click)=\"selectCourseForm(course)\">{{course}}</a>\n            </div>\n          </div>\n        </div>\n\n      </div>\n\n      <!-- Submit -->\n      <div class=\"d-flex justify-content-center mt-2\">\n        <button (click)=\"addNewHomework()\" class=\"btn btn-outline-danger\">Submit</button>\n      </div>\n\n    </div>\n  </div>\n\n\n</div>\n\n\n"

/***/ }),

/***/ "../../../../../src/app/app.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__course_service__ = __webpack_require__("../../../../../src/app/course.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var AppComponent = (function () {
    function AppComponent(_courseService) {
        this._courseService = _courseService;
    }
    AppComponent.prototype.ngOnInit = function () {
        this.specialisationsByYear = this._courseService.getYearsWithSpecialisations();
        this.showAddForm = false;
    };
    AppComponent.prototype.updateHomework = function () {
        var _this = this;
        if (!this.selectedYear || !this.selectedSpecialisation) {
            return;
        }
        this._courseService.getHomework(this.selectedYear, this.selectedSpecialisation)
            .subscribe(function (res) {
            _this.homeworkList = res;
        });
    };
    AppComponent.prototype.getYears = function () {
        return Object.keys(this.specialisationsByYear);
    };
    AppComponent.prototype.getSpecialisations = function () {
        if (this.selectedYear) {
            return this.specialisationsByYear[this.selectedYear];
        }
        return null;
    };
    AppComponent.prototype.selectYear = function (year) {
        this.selectedYear = year;
        console.log("Selected year " + year);
    };
    AppComponent.prototype.selectSpecialisation = function (specialisation) {
        this.selectedSpecialisation = specialisation;
        console.log("Selected specialisation " + specialisation);
        this.updateHomework();
    };
    /////////// Methods for adding new homework
    AppComponent.prototype.getSpecialisationsForm = function () {
        if (this.selectedYearForm) {
            return this.specialisationsByYear[this.selectedYearForm];
        }
        return null;
    };
    AppComponent.prototype.selectYearForm = function (year) {
        this.selectedYearForm = year;
        console.log("Selected year " + year);
    };
    AppComponent.prototype.selectSpecialisationForm = function (specialisation) {
        this.selectedSpecialisationForm = specialisation;
        console.log("Selected specialisation " + specialisation);
        this.updateHomeworkForm();
    };
    AppComponent.prototype.selectCourseForm = function (course) {
        this.selectedCourseForm = course;
    };
    AppComponent.prototype.updateHomeworkForm = function () {
        var _this = this;
        this._courseService.getHomework(this.selectedYearForm, this.selectedSpecialisationForm)
            .subscribe(function (res) {
            _this.homeworkListForm = res;
            _this.updateCoursesForm();
        });
    };
    AppComponent.prototype.updateCoursesForm = function () {
        this.courses = this.homeworkListForm.map(function (h) { return h["courseName"]; });
        console.log("courses " + this.courses);
    };
    AppComponent.prototype.addNewHomework = function () {
        var _this = this;
        var newHomework = this.homeworkListForm.find(function (h) { return h["courseName"] === _this.selectedCourseForm; });
        if (newHomework) {
            this.homeworkList.push(newHomework);
        }
        this.selectedCourseForm = undefined;
        this.selectedYearForm = undefined;
        this.selectedSpecialisationForm = undefined;
        this.showAddForm = false;
    };
    AppComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["m" /* Component */])({
            selector: 'app-root',
            template: __webpack_require__("../../../../../src/app/app.component.html"),
            styles: [__webpack_require__("../../../../../src/app/app.component.css")]
        }),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1__course_service__["a" /* CourseService */]])
    ], AppComponent);
    return AppComponent;
}());



/***/ }),

/***/ "../../../../../src/app/app.module.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__ = __webpack_require__("../../../platform-browser/esm5/platform-browser.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_common_http__ = __webpack_require__("../../../common/esm5/http.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__app_component__ = __webpack_require__("../../../../../src/app/app.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__course_service__ = __webpack_require__("../../../../../src/app/course.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__homework_detail_homework_detail_component__ = __webpack_require__("../../../../../src/app/homework-detail/homework-detail.component.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};






var AppModule = (function () {
    function AppModule() {
    }
    AppModule = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_2__angular_core__["E" /* NgModule */])({
            declarations: [
                __WEBPACK_IMPORTED_MODULE_3__app_component__["a" /* AppComponent */],
                __WEBPACK_IMPORTED_MODULE_5__homework_detail_homework_detail_component__["a" /* HomeworkDetailComponent */]
            ],
            imports: [
                __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__["a" /* BrowserModule */],
                __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["b" /* HttpClientModule */]
            ],
            providers: [__WEBPACK_IMPORTED_MODULE_4__course_service__["a" /* CourseService */]],
            bootstrap: [__WEBPACK_IMPORTED_MODULE_3__app_component__["a" /* AppComponent */]]
        })
    ], AppModule);
    return AppModule;
}());



/***/ }),

/***/ "../../../../../src/app/course.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return CourseService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_common_http__ = __webpack_require__("../../../common/esm5/http.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


var CourseService = (function () {
    function CourseService(_http) {
        this._http = _http;
        this.backendUrl = '192.168.0.103:3000';
    }
    CourseService.prototype.getYearsWithSpecialisations = function () {
        var specialisationByYear = {
            1: ['CA', 'CB', 'CC'],
            2: ['CA', 'CB', 'CC'],
            3: ['CA', 'CB', 'CC'],
            4: ['C1', 'C2', 'C3', 'C4', 'C5'],
            5: ['SCPD', 'IA', 'SSA', 'MTI', 'eGOV'],
            6: ['SCPD', 'IA', 'SSA', 'MTI', 'eGOV']
        };
        return specialisationByYear;
    };
    CourseService.prototype.getHomework = function (year, specialisation) {
        return this._http.get('http://localhost:3000/get-homework', {
            params: new __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["c" /* HttpParams */]().set('year', year).set('specialisation', specialisation),
        });
    };
    CourseService = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["w" /* Injectable */])(),
        __metadata("design:paramtypes", [__WEBPACK_IMPORTED_MODULE_1__angular_common_http__["a" /* HttpClient */]])
    ], CourseService);
    return CourseService;
}());



/***/ }),

/***/ "../../../../../src/app/homework-detail/homework-detail.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".deadlines {\n\n}\n\n.erase {\n  text-align: end;\n}\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/homework-detail/homework-detail.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"list-group-item list-group-item-action flex-column align-items-center container\" *ngIf=\"homework && display\">\n  <div class=\"row justify-content-center\">\n    <div class=\"col-5\">\n      <h5>{{homework[\"homeworkName\"]}}</h5>\n      <h6>{{homework[\"courseName\"]}}</h6>\n    </div>\n\n    <div class=\"col-5 deadlines\">\n      <div class=\"float-left\">Deadline soft:&nbsp;</div> <div class=\"font-weight-bold float-left\">{{homework[\"deadlineSoft\"] | date:'dd-MM-yyyy'}}</div><br/>\n      <div>Deadline hard: {{homework[\"deadlineHard\"] | date:'dd-MM-yyyy'}}</div>\n    </div>\n\n    <div class=\"col-2 erase text-muted\">\n      <a href=\"#\" (click)=\"eraseEntry()\">Erase</a>\n    </div>\n  </div>\n\n\n</div>\n"

/***/ }),

/***/ "../../../../../src/app/homework-detail/homework-detail.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return HomeworkDetailComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

var HomeworkDetailComponent = (function () {
    function HomeworkDetailComponent() {
    }
    HomeworkDetailComponent.prototype.ngOnInit = function () {
        this.display = true;
    };
    HomeworkDetailComponent.prototype.eraseEntry = function () {
        this.display = false;
    };
    __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["z" /* Input */])(),
        __metadata("design:type", Object)
    ], HomeworkDetailComponent.prototype, "homework", void 0);
    HomeworkDetailComponent = __decorate([
        Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["m" /* Component */])({
            selector: 'homework-detail',
            template: __webpack_require__("../../../../../src/app/homework-detail/homework-detail.component.html"),
            styles: [__webpack_require__("../../../../../src/app/homework-detail/homework-detail.component.css")],
            encapsulation: __WEBPACK_IMPORTED_MODULE_0__angular_core__["_2" /* ViewEncapsulation */].None
        }),
        __metadata("design:paramtypes", [])
    ], HomeworkDetailComponent);
    return HomeworkDetailComponent;
}());



/***/ }),

/***/ "../../../../../src/environments/environment.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return environment; });
// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.
var environment = {
    production: false
};


/***/ }),

/***/ "../../../../../src/main.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/esm5/core.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_platform_browser_dynamic__ = __webpack_require__("../../../platform-browser-dynamic/esm5/platform-browser-dynamic.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__app_app_module__ = __webpack_require__("../../../../../src/app/app.module.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__environments_environment__ = __webpack_require__("../../../../../src/environments/environment.ts");




if (__WEBPACK_IMPORTED_MODULE_3__environments_environment__["a" /* environment */].production) {
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_5" /* enableProdMode */])();
}
Object(__WEBPACK_IMPORTED_MODULE_1__angular_platform_browser_dynamic__["a" /* platformBrowserDynamic */])().bootstrapModule(__WEBPACK_IMPORTED_MODULE_2__app_app_module__["a" /* AppModule */])
    .catch(function (err) { return console.log(err); });


/***/ }),

/***/ 0:
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__("../../../../../src/main.ts");


/***/ })

},[0]);
//# sourceMappingURL=main.bundle.js.map