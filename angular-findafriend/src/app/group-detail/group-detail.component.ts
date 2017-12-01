import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-group-detail',
  templateUrl: './group-detail.component.html',
  styleUrls: ['./group-detail.component.css']
})
export class GroupDetailComponent implements OnInit {
	@Input() group: any;
  @Input() username:string;
	@Input() inGroup:boolean;
  showMembers = null;

  constructor(
  ) { }

  ngOnInit(){

  }


  seeMembers(){
  	if (this.showMembers == null){
  		this.showMembers = true;

  	}
  	else{
  		this.showMembers = null;
  		document.getElementById("memButton").innerHTML = this.group.members.length +" Members (Show)";
  	}
  }



  addToGroup(){
    //Post data to django to add name to list
  }

}
