import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'SimilarityApp';
}

export class YourComponent {
  inputPhrase: string = '';
  referenceSentences: string[] = [];
  similarities: number[] = [];

  constructor(private http: HttpClient) {}

  calculateSimilarity() {
    const payload = {
      input_phrase: this.inputPhrase
    };

    this.http.post<any>('/api/similarity', payload).subscribe(
      (response) => {
        this.referenceSentences = response.reference_sentences;
        this.similarities = response.similarities;
      },
      (error) => {
        console.log('Error:', error);
      }
    );
  }
}
