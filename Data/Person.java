//v28. Person class of IMSHED
//Author: Li An
//Starting date: Feb 25, 2004; ending date: Feb 26, 2004.
//Last modified: Dec 27, 2007; 11-20-2008

import java.io.*;//import this b/c FileReader is used
import java.util.*;//import this b/c List is used
import swarm.Globals;
import swarm.defobj.Zone;
import swarm.objectbase.SwarmObjectImpl;

public class Person extends SwarmObjectImpl{
    public int id,age,hsId,education,gender,momId,dadId,spouseStatus;
    public int birthPlan;//# of children to have
    int birthYear;
    public int birthInterval; //years between two consecutive births
    public int maxBirthInterval;
    public int maxFirstKidInterval;
    public int firstKidInterval;//years between marriage and birth of 1st kid.
    public double numOfKids;
    public int marryYear;
    public double relationIndex;
    String temp="";
    int temp1;
    char temp2;
    double temp3;
   
    public Person(Zone aZone, int maxBirthInt, double numKids,
		  int maxFirstKidInt){
	super(aZone);
	maxBirthInterval=maxBirthInt;
	numOfKids=numKids;
	maxFirstKidInterval=maxFirstKidInt;
    }

    public void setId(int x){
	id=x;
    }
    public int getId(){	
	return id;
    }

    public void setBirthInterval(){
	birthInterval=SwarmUtils.getRandIntWithMinMax(1,maxBirthInterval);
    }
    public int  getBirthInterval(){
	return birthInterval;
    }

    public void setFirstKidInterval(){
	firstKidInterval=SwarmUtils.getRandIntWithMinMax
	    (1,maxFirstKidInterval);//back to 5
    }
    public int  getFirstKidInterval(){
	return firstKidInterval;
    }
   
    public void setBirthPlan(){
	if(numOfKids==2.5){
	    temp3=Math.random();

	    /* the key is to let the average # of childs to be 2.5 (Liu et al 
	    1999, P&E paper). The numbers come from a binomial distribution 
	    with p=0.5 and N=5.*/

	    if(temp3<0.03125){
		birthPlan=0;
	    }
	    else if(temp3>=0.03125 && temp3<0.1875){
		birthPlan=1;
	    }
	    else if(temp3>=0.1875 && temp3<0.5){
		birthPlan=2; 
	    }
	    else if(temp3>=0.5 && temp3<0.8125){
		birthPlan=3;	   
	    }
	    else if(temp3>=0.8125 && temp3<0.96875){
		birthPlan=4;	  
	    }
	    else{
		birthPlan=5;	  
	    }
	}
	else{
	    birthPlan=SwarmUtils.getRandIntWithMinMax(0,(int)numOfKids*2);
	}
    }        
    
    public int getBirthPlan(){	
	return birthPlan;
    }

    public void setMarryYear(int x){
	marryYear=x;
    }
    public int getMarryYear(){
	return marryYear;
    }

    public void setBirthYear(int x){
	birthYear=x;
    }
    public int getBirthYear(){
	return birthYear;
    }    

    public void setMomId(int x){
	momId=x;
    }
    public int getMomId(){
	return momId;
    } 

    public void setDadId(int x){
	dadId=x;
    }
    public int getDadId(){
	return dadId;
    }

    public void setSpouseStatus(int x){
	spouseStatus=x;
    }
    public int getSpouseStatus(){
	return spouseStatus;
    }

    public void setRelationIndex(double x){
	relationIndex=x;
    }  
    public double getRelationIndex(){
	return relationIndex;
    }

    public void setAge(int x){
	age=x;
    }  
    public int getAge(){
	return age;
    }

    public void setHsId(int x){
	hsId=x;
    }  
    public int getHsId(){
	return hsId;
    }

    public void setEducation(int x){
	education=x;
    }  
    public int getEducation(){
	return education;
    }

    public void setGender(int x){
	gender=x;
    }  
    public int getGender(){
	return gender;
    }

    public void loadPsnData(FileReader f){
	try{
	    for (int i=0;i<9;i++){//why 9? have 9 variables for each person
		temp2=(char)f.read();
		temp="";
		
		while(temp2!=',' && temp2!='\n'){
		    temp+=temp2;
		    temp2=(char)f.read();//moved to the comma or return
		    if(i==0){setId(Integer.parseInt(temp));}
		    if(i==1){setAge(Integer.parseInt(temp));}
		    if(i==2){setHsId(Integer.parseInt(temp));}
		    if(i==3){setEducation(Integer.parseInt(temp));}
		    if(i==4){setGender(Integer.parseInt(temp));}
		    if(i==5){setRelationIndex(Double.parseDouble(temp));}
		    if(i==6){setMomId(Integer.parseInt(temp));}
		    if(i==7){setDadId(Integer.parseInt(temp));}
		    if(i==8){setSpouseStatus(Integer.parseInt(temp));}
		}
	    }
	}

	catch(Exception e){
	    System.out.println("Error loading persons: "+e);
	    System.exit(0);
	}		
    }
     
    public List death(List theList, int year){ 
	theList.remove(this);
	//System.out.println("Sorry, one person dies at year "+year);
	return theList;
	}

    public List educationMoveOut(List theList,int year){
	theList.remove(this);
	//System.out.println("Good! a person goes to college at year "+year);
	return theList;
    }

    public void reportAge(int year){
	System.out.println("At year "+year+", "+
			   "person "+ this.getId()+"'s age is "+this.getAge());
    }
}

