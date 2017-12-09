import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
	public loading = true;
  	title = 'Find a Friend';

  	ngOnInit(){
		this.loading = false;
		
	}


}
