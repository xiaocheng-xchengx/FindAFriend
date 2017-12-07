import { Component, OnInit, Input } from '@angular/core';
import {Group} from '../group';
import {GROUPS} from '../list-of-groups';
// import { GroupServiceService } from '../group-service.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-groups',
  templateUrl: './groups.component.html',
  styleUrls: ['./groups.component.css']
})
export class GroupsComponent implements OnInit {

  @Input() username:string;
  groups :any;
  displayGroups: any = [];
  selectedGroup:any;
  selectedGroupCreator:any;
  inGroup:boolean = false;
  searchTerm = null;

  constructor(private http: HttpClient) { }

  ngOnInit() {
  	this.getGroups();
  	this.getUsername();
    console.log(this.username);
  }

  alert(msg?: string)      { window.alert(msg); }
  canSave=true;

  getUsername():void{
    var i:number = 0;
    for(i ; i <this.groups.length;i++){
      // Change creator url to username
      this.http.get(this.groups[i].creator).subscribe(data => {
        this.groups[i].creator = (data as any).username;
      })
    }
  }



  /* GET GROUPS FROM BACKEND */
  getGroups():void{

    let url :string;
    url = "/api/pages/?format=json";

    console.log(url);

  	this.http.get(url).subscribe(data => {
      // let obj = Group: JSON.parse(data);
      // console.log(obj.title);
      this.groups = data;
      console.log(this.groups);
    })


  }

  onSelect(group:any):void{
    // console.log("ayyyy");
    // this.selectedGroup.creator = this.selectedGroupCreator.username;
    // let idx = 0;//this.groups.indexOf(group);
    this.getGroups();
    

    let groupA;
    for (let u of this.groups){
      if (u.title == group.title){
        groupA = u;
      }
    }

    this.selectedGroup = groupA;

    this.checkInGroup();
  }

  removefromList(g){
    console.log("----------ok-----------");
    var i:number = 0;
    for(i ; i < this.displayGroups.length;i++){
      if (this.displayGroups[i].title == g.title){
         this.displayGroups.splice(i,1);
      }
    } 
  }

  checkInGroup(){
    for (let u of this.selectedGroup.members){
      if (u.username == this.username){
        console.log("gucci");
        this.inGroup = true;
        return;
      }
    }
    console.log(this.username);
    console.log("nahh");
    this.inGroup=false;
  
  }

  addGroup(group:Group){
    this.alert(`Join ${group ? group.title : 'this group'}.`);
  }


  /* SEARCH BAR */
  onKey(value:String):void{
    this.searchTerm = value;
    this.displayGroups = [];
    var notSelected: any = [];
    var notSelected2: any = [];
    console.log("re-checked");

    var i:number = 0;

    for(i ; i < this.groups.length;i++){         //Search for title match first
      if((this.groups[i].title.toLowerCase()).search(value.toLowerCase()) != -1){
        // Change creator url to username
        this.http.get(this.groups[i].creator).subscribe(data => {
          this.groups[i].creator = (data as any).username;
        })
        this.displayGroups.push(this.groups[i]);
        console.log(this.displayGroups);
      }
      else{
        notSelected.push(this.groups[i]);
      }
    }

    i =0;
    for(i ; i < notSelected.length;i++){       //Search for typeOfGroup next
      if((notSelected[i].typeOfGroup.toLowerCase()).search(value.toLowerCase()) != -1){
        // Change creator url to username
        this.http.get(this.groups[i].creator).subscribe(data => {
          this.groups[i].creator = (data as any).username;
        })
        this.displayGroups.push(notSelected[i]);
        console.log(this.displayGroups);
      }
      else{
        notSelected2.push(notSelected[i]);
      }
    }

    notSelected = [];
    i=0;
    for(i ; i < notSelected2.length;i++){      //Search for creator next
      if((notSelected2[i].creator.toLowerCase()).search(value.toLowerCase()) != -1){
        // Change creator url to username
        this.http.get(this.groups[i].creator).subscribe(data => {
          this.groups[i].creator = (data as any).username;
        })
        this.displayGroups.push(notSelected2[i]);
        console.log(this.displayGroups);
      }
      else{
        notSelected.push(notSelected2[i]);
      }
    }

    i=0;

    for(i ; i < notSelected.length;i++){         //Search for description next
      if((notSelected[i].description.toLowerCase()).search(value.toLowerCase()) != -1){
        // Change creator url to username
        this.http.get(this.groups[i].creator).subscribe(data => {
          this.groups[i].creator = (data as any).username;
        })
        this.displayGroups.push(notSelected[i]);
        console.log(this.displayGroups);
      }
    }




    console.log(value);

  }

}
