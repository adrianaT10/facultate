import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs/Rx';
import { of } from 'rxjs/observable/of';

@Injectable()
export class CourseService {

  constructor(private _http: HttpClient) { }

  getYearsWithSpecialisations(): object {
    let specialisationByYear = {
      1: ['CA', 'CB', 'CC'],
      2: ['CA', 'CB', 'CC'],
      3: ['CA', 'CB', 'CC'],
      4: ['C1', 'C2', 'C3', 'C4', 'C5'],
      5: ['SCPD', 'IA', 'SSA', 'MTI', 'eGOV'],
      6: ['SCPD', 'IA', 'SSA', 'MTI', 'eGOV']
    };

    return specialisationByYear;
  }

  getHomework(year, specialisation) {
    return this._http.get('/get-homework', {
      params: new HttpParams().set('year', year).set('specialisation', specialisation),
    });
  }
}
