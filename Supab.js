// server.js (CommonJS)
const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 8000;

app.use(cors());
app.use(bodyParser.json());

// ----------------------
// Valid Tokens
// ----------------------
const validTokens = new Set([
  "token_fb_abc123",
  "token_fb_demo",
  "token_ig_abc123",
  "token_ig_demo"
]);

// ----------------------
// Dummy FB Users (20 users with friends and location)
// ----------------------
const fbBaseId = "122094043977116573"; // string
const fbUsers = [];
const fbUserMap = {};

const fbNames = [
  { firstName: "Manoj", lastName: "Shakya", age: 25, dob: "05/07/1999", user_location: "Kanpur, India" },
  { firstName: "Himanshu", lastName: "Yadav", age: 26, dob: "12/03/1998", user_location: "Noida, India" },
  { firstName: "Jyoti", lastName: "Shakya", age: 24, dob: "11/08/1999", user_location: "Lucknow, India" },
  { firstName: "Anshu", lastName: "Patel", age: 27, dob: "05/06/1997", user_location: "Ahmedabad, India" },
  { firstName: "Mohit", lastName: "Kumar", age: 25, dob: "23/09/1999", user_location: "Bangalore, India" },
  { firstName: "Rohit", lastName: "Verma", age: 28, dob: "15/02/1996", user_location: "Pune, India" },
  { firstName: "Neha", lastName: "Kumar", age: 23, dob: "30/01/2000", user_location: "Chennai, India" },
  { firstName: "Sara", lastName: "Ali", age: 22, dob: "12/12/2001", user_location: "Hyderabad, India" },
  { firstName: "Aman", lastName: "Gupta", age: 29, dob: "09/11/1995", user_location: "Kolkata, India" },
  { firstName: "Pooja", lastName: "Sharma", age: 26, dob: "17/07/1997", user_location: "Mumbai, India" },
  { firstName: "Ravi", lastName: "Patel", age: 28, dob: "05/03/1995", user_location: "Jaipur, India" },
  { firstName: "Ankit", lastName: "Sharma", age: 27, dob: "22/04/1996", user_location: "Lucknow, India" },
  { firstName: "Priya", lastName: "Singh", age: 24, dob: "10/10/1999", user_location: "Delhi, India" },
  { firstName: "Karan", lastName: "Gupta", age: 25, dob: "05/06/1999", user_location: "Noida, India" },
  { firstName: "Simran", lastName: "Kaur", age: 23, dob: "29/08/2000", user_location: "Chandigarh, India" },
  { firstName: "Aakash", lastName: "Verma", age: 27, dob: "11/11/1996", user_location: "Bangalore, India" },
  { firstName: "Neelam", lastName: "Sharma", age: 22, dob: "14/12/2001", user_location: "Hyderabad, India" },
  { firstName: "Suresh", lastName: "Yadav", age: 28, dob: "07/05/1995", user_location: "Gurgaon, India" },
  { firstName: "Anjali", lastName: "Patel", age: 26, dob: "03/03/1997", user_location: "Ahmedabad, India" },
  { firstName: "Mohini", lastName: "Kumar", age: 25, dob: "19/09/1999", user_location: "Pune, India" },

  { firstName: "Vikas", lastName: "Sharma", age: 27, dob: "08/01/1997", user_location: "Varanasi, India" },
  { firstName: "Arjun", lastName: "Singh", age: 23, dob: "22/09/2001", user_location: "Kanpur, India" },
  { firstName: "Ritika", lastName: "Kapoor", age: 21, dob: "01/03/2003", user_location: "Indore, India" },
  { firstName: "Sahil", lastName: "Jain", age: 30, dob: "25/12/1993", user_location: "Delhi, India" },
  { firstName: "Sneha", lastName: "Rajput", age: 28, dob: "17/05/1996", user_location: "Udaipur, India" },
  { firstName: "Yogesh", lastName: "Thakur", age: 26, dob: "14/08/1998", user_location: "Gwalior, India" },
  { firstName: "Kajal", lastName: "Pandey", age: 25, dob: "07/02/1999", user_location: "Patna, India" },
  { firstName: "Naman", lastName: "Joshi", age: 29, dob: "30/10/1995", user_location: "Raipur, India" },
  { firstName: "Riya", lastName: "Mehta", age: 22, dob: "06/06/2002", user_location: "Delhi, India" },
  { firstName: "Harsh", lastName: "Bansal", age: 27, dob: "19/04/1997", user_location: "Mumbai, India" },

  { firstName: "Divya", lastName: "Saxena", age: 24, dob: "11/11/1999", user_location: "Bhopal, India" },
  { firstName: "Lakshay", lastName: "Arora", age: 23, dob: "02/05/2001", user_location: "Pune, India" },
  { firstName: "Ishita", lastName: "Rana", age: 21, dob: "21/02/2003", user_location: "Amritsar, India" },
  { firstName: "Ashutosh", lastName: "Nair", age: 28, dob: "07/07/1996", user_location: "Kochi, India" },
  { firstName: "Nidhi", lastName: "Shrivastav", age: 25, dob: "28/01/1999", user_location: "Nagpur, India" },
  { firstName: "Virat", lastName: "Shetty", age: 29, dob: "16/06/1995", user_location: "Bangalore, India" },
  { firstName: "Sonia", lastName: "Matthew", age: 24, dob: "09/09/2000", user_location: "Goa, India" },
  { firstName: "Ajay", lastName: "Chopra", age: 27, dob: "12/08/1997", user_location: "Jodhpur, India" },
  { firstName: "Meera", lastName: "Sethi", age: 26, dob: "18/03/1998", user_location: "Jaipur, India" },
  { firstName: "Dev", lastName: "Gill", age: 30, dob: "04/12/1993", user_location: "Chandigarh, India" },

  { firstName: "Shivam", lastName: "Prajapati", age: 25, dob: "14/04/1999", user_location: "Agra, India" },
  { firstName: "Payal", lastName: "Mishra", age: 23, dob: "20/10/2000", user_location: "Mirzapur, India" },
  { firstName: "Gaurav", lastName: "Tripathi", age: 27, dob: "09/08/1997", user_location: "Basti, India" },
  { firstName: "Aisha", lastName: "Khan", age: 24, dob: "01/02/2000", user_location: "Lucknow, India" },
  { firstName: "Farhan", lastName: "Javed", age: 29, dob: "13/05/1995", user_location: "Delhi, India" },
  { firstName: "Tamanna", lastName: "Borah", age: 22, dob: "21/12/2001", user_location: "Guwahati, India" },
  { firstName: "Rohan", lastName: "Das", age: 26, dob: "27/07/1998", user_location: "Kolkata, India" },
  { firstName: "Roshni", lastName: "Dutta", age: 25, dob: "08/09/1999", user_location: "Kolkata, India" },
  { firstName: "Kabir", lastName: "Chatterjee", age: 28, dob: "05/05/1996", user_location: "Kolkata, India" },
  { firstName: "Aditya", lastName: "Rathore", age: 26, dob: "22/03/1998", user_location: "Ajmer, India" },

  { firstName: "Muskan", lastName: "Sahu", age: 23, dob: "15/01/2001", user_location: "Raipur, India" },
  { firstName: "Devesh", lastName: "Mannan", age: 27, dob: "11/10/1997", user_location: "Delhi, India" },
  { firstName: "Sunita", lastName: "Rawat", age: 29, dob: "30/06/1995", user_location: "Dehradun, India" },
  { firstName: "Kunal", lastName: "Bhardwaj", age: 24, dob: "19/11/1999", user_location: "Noida, India" },
  { firstName: "Tanvi", lastName: "Malhotra", age: 23, dob: "03/04/2001", user_location: "Delhi, India" },
  { firstName: "Sarika", lastName: "Goswami", age: 28, dob: "12/12/1996", user_location: "Bhubaneswar, India" },
  { firstName: "Prakash", lastName: "Jha", age: 30, dob: "07/01/1994", user_location: "Patna, India" },
  { firstName: "Alok", lastName: "Singhania", age: 27, dob: "25/05/1997", user_location: "Ranchi, India" },
  { firstName: "Esha", lastName: "Kapoor", age: 21, dob: "18/09/2003", user_location: "Delhi, India" },
  { firstName: "Ramesh", lastName: "Bhatt", age: 29, dob: "09/10/1995", user_location: "Haridwar, India" },
  { firstName: "Aarav", lastName: "Kapoor", age: 24, dob: "12/02/2000", user_location: "Delhi, India" },
  { firstName: "Isha", lastName: "Chawla", age: 23, dob: "14/07/2001", user_location: "Mumbai, India" },
  { firstName: "Rudra", lastName: "Reddy", age: 28, dob: "21/06/1996", user_location: "Hyderabad, India" },
  { firstName: "Kavya", lastName: "Shekhar", age: 25, dob: "09/11/1999", user_location: "Bangalore, India" },
  { firstName: "Niharika", lastName: "Soni", age: 22, dob: "04/01/2002", user_location: "Jaipur, India" },
  { firstName: "Harshit", lastName: "Dubey", age: 29, dob: "18/05/1995", user_location: "Indore, India" },
  { firstName: "Rehan", lastName: "Ansari", age: 26, dob: "15/03/1998", user_location: "Lucknow, India" },
  { firstName: "Tanya", lastName: "Roy", age: 24, dob: "27/09/1999", user_location: "Kolkata, India" },
  { firstName: "Zoya", lastName: "Pathan", age: 21, dob: "06/06/2003", user_location: "Pune, India" },
  { firstName: "Arnav", lastName: "Saxena", age: 30, dob: "19/12/1993", user_location: "Chandigarh, India" },

  { firstName: "Mitali", lastName: "Chatterjee", age: 23, dob: "13/08/2001", user_location: "Kolkata, India" },
  { firstName: "Param", lastName: "Gill", age: 27, dob: "02/10/1997", user_location: "Amritsar, India" },
  { firstName: "Vidhi", lastName: "Agarwal", age: 25, dob: "10/04/1999", user_location: "Ahmedabad, India" },
  { firstName: "Krish", lastName: "Nanda", age: 22, dob: "08/01/2002", user_location: "Surat, India" },
  { firstName: "Avantika", lastName: "Rawal", age: 26, dob: "17/03/1998", user_location: "Vadodara, India" },
  { firstName: "Samar", lastName: "Grewal", age: 29, dob: "01/12/1995", user_location: "Delhi, India" },
  { firstName: "Ananya", lastName: "Deshmukh", age: 24, dob: "05/05/2000", user_location: "Nagpur, India" },
  { firstName: "Shaurya", lastName: "Tiwari", age: 23, dob: "11/06/2001", user_location: "Bhopal, India" },
  { firstName: "Aditi", lastName: "Kulkarni", age: 27, dob: "29/09/1997", user_location: "Goa, India" },
  { firstName: "Mehul", lastName: "Purohit", age: 28, dob: "14/02/1996", user_location: "Rajasthan, India" },

  { firstName: "Shreya", lastName: "Mahajan", age: 22, dob: "02/02/2002", user_location: "Udaipur, India" },
  { firstName: "Dhruv", lastName: "Chandel", age: 26, dob: "16/06/1998", user_location: "Shimla, India" },
  { firstName: "Laiba", lastName: "Naseer", age: 24, dob: "20/10/2000", user_location: "Delhi, India" },
  { firstName: "Ritesh", lastName: "Giri", age: 25, dob: "09/01/1999", user_location: "Ranchi, India" },
  { firstName: "Anusha", lastName: "Pillai", age: 23, dob: "03/11/2001", user_location: "Kochi, India" },
  { firstName: "Yuvraj", lastName: "Bose", age: 28, dob: "30/05/1996", user_location: "Howrah, India" },
  { firstName: "Mahira", lastName: "Iqbal", age: 21, dob: "12/07/2003", user_location: "Srinagar, India" },
  { firstName: "Faisal", lastName: "Haque", age: 24, dob: "05/04/2000", user_location: "Patna, India" },
  { firstName: "Preeti", lastName: "Goyal", age: 29, dob: "22/03/1995", user_location: "Delhi, India" },
  { firstName: "Shaheen", lastName: "Ali", age: 27, dob: "03/12/1997", user_location: "Hyderabad, India" },

  { firstName: "Ayaan", lastName: "Mohammed", age: 23, dob: "14/06/2001", user_location: "Bangalore, India" },
  { firstName: "Nikita", lastName: "Awasthi", age: 25, dob: "18/01/1999", user_location: "Kanpur, India" },
  { firstName: "Sarthak", lastName: "Lohani", age: 26, dob: "19/09/1998", user_location: "Dehradun, India" },
  { firstName: "Avantika", lastName: "Vyas", age: 22, dob: "02/05/2002", user_location: "Ujjain, India" },
  { firstName: "Devika", lastName: "Nair", age: 29, dob: "04/04/1995", user_location: "Kochi, India" },
  { firstName: "Keshav", lastName: "Bhargava", age: 30, dob: "10/08/1994", user_location: "Delhi, India" },
  { firstName: "Ansh", lastName: "Khatri", age: 24, dob: "05/01/2000", user_location: "Gurgaon, India" },
  { firstName: "Riddhi", lastName: "Sharma", age: 22, dob: "09/11/2002", user_location: "Noida, India" },
  { firstName: "Samaira", lastName: "Chopra", age: 23, dob: "16/10/2001", user_location: "Mumbai, India" },
  { firstName: "Hardik", lastName: "Solanki", age: 28, dob: "09/07/1996", user_location: "Rajkot, India" },

  { firstName: "Tushar", lastName: "Kohli", age: 26, dob: "07/06/1998", user_location: "Pune, India" },
  { firstName: "Mira", lastName: "Salvi", age: 25, dob: "21/09/1999", user_location: "Surat, India" },
  { firstName: "Varun", lastName: "Pandya", age: 27, dob: "13/12/1997", user_location: "Baroda, India" },
  { firstName: "Sia", lastName: "Bhandari", age: 21, dob: "05/03/2003", user_location: "Delhi, India" },
  { firstName: "Eklavya", lastName: "Tripathi", age: 24, dob: "08/08/2000", user_location: "Gorakhpur, India" },
  { firstName: "Arohi", lastName: "Dubey", age: 23, dob: "27/04/2001", user_location: "Lucknow, India" },
  { firstName: "Harsh", lastName: "Chauhan", age: 26, dob: "14/02/1998", user_location: "Delhi, India" },
  { firstName: "Divya", lastName: "Rana", age: 23, dob: "21/09/2001", user_location: "Pune, India" },
  { firstName: "Sumit", lastName: "Kapoor", age: 27, dob: "02/07/1997", user_location: "Noida, India" },
  { firstName: "Ritika", lastName: "Mishra", age: 24, dob: "11/01/2000", user_location: "Kanpur, India" },
  { firstName: "Gaurav", lastName: "Saxena", age: 29, dob: "28/08/1995", user_location: "Agra, India" },
  { firstName: "Nidhi", lastName: "Jain", age: 22, dob: "15/04/2002", user_location: "Bhopal, India" },
  { firstName: "Yash", lastName: "Bansal", age: 25, dob: "19/10/1999", user_location: "Indore, India" },
  { firstName: "Tina", lastName: "Roy", age: 23, dob: "04/12/2001", user_location: "Kolkata, India" },
  { firstName: "Shivam", lastName: "Tiwari", age: 28, dob: "08/06/1996", user_location: "Lucknow, India" },
  { firstName: "Poonam", lastName: "Saini", age: 24, dob: "07/03/2000", user_location: "Ambala, India" },

  { firstName: "Vikas", lastName: "Kumar", age: 27, dob: "11/09/1997", user_location: "Patna, India" },
  { firstName: "Shruti", lastName: "Goyal", age: 22, dob: "03/02/2002", user_location: "Jaipur, India" },
  { firstName: "Rahul", lastName: "Bhardwaj", age: 26, dob: "16/05/1998", user_location: "Delhi, India" },
  { firstName: "Megha", lastName: "Soni", age: 25, dob: "09/11/1999", user_location: "Udaipur, India" },
  { firstName: "Alok", lastName: "Yadav", age: 28, dob: "05/07/1996", user_location: "Gurgaon, India" },
  { firstName: "Karishma", lastName: "Sharma", age: 23, dob: "27/01/2001", user_location: "Shimla, India" },
  { firstName: "Deepak", lastName: "Verma", age: 29, dob: "22/08/1995", user_location: "Chandigarh, India" },
  { firstName: "Sakshi", lastName: "Khanna", age: 24, dob: "18/03/2000", user_location: "Amritsar, India" },
  { firstName: "Aditya", lastName: "Nigam", age: 25, dob: "13/10/1999", user_location: "Prayagraj, India" },
  { firstName: "Rekha", lastName: "Gupta", age: 26, dob: "30/06/1998", user_location: "Moradabad, India" },

  { firstName: "Naman", lastName: "Rathod", age: 24, dob: "12/05/2000", user_location: "Nagpur, India" },
  { firstName: "Jasmin", lastName: "Kaur", age: 22, dob: "26/12/2002", user_location: "Ludhiana, India" },
  { firstName: "Sahil", lastName: "Chhabra", age: 27, dob: "08/04/1997", user_location: "Delhi, India" },
  { firstName: "Kajal", lastName: "Gill", age: 23, dob: "02/02/2001", user_location: "Jalandhar, India" },
  { firstName: "Ajeet", lastName: "Rawat", age: 28, dob: "21/03/1996", user_location: "Ghaziabad, India" },
  { firstName: "Monika", lastName: "Chauhan", age: 25, dob: "14/07/1999", user_location: "Panipat, India" },
  { firstName: "Harshit", lastName: "Agarwal", age: 26, dob: "18/09/1998", user_location: "Aligarh, India" },
  { firstName: "Shraddha", lastName: "Seth", age: 24, dob: "05/01/2000", user_location: "Vadodara, India" },
  { firstName: "Raj", lastName: "Solanki", age: 29, dob: "09/08/1995", user_location: "Surat, India" },
  { firstName: "Meera", lastName: "Desai", age: 23, dob: "11/11/2001", user_location: "Rajkot, India" },

  { firstName: "Ashish", lastName: "Pandit", age: 26, dob: "03/03/1998", user_location: "Nashik, India" },
  { firstName: "Pallavi", lastName: "Joshi", age: 25, dob: "28/09/1999", user_location: "Thane, India" },
  { firstName: "Rohan", lastName: "Kulkarni", age: 27, dob: "17/04/1997", user_location: "Pune, India" },
  { firstName: "Sneha", lastName: "More", age: 22, dob: "24/12/2001", user_location: "Mumbai, India" },
  { firstName: "Imran", lastName: "Sheikh", age: 28, dob: "02/10/1996", user_location: "Hyderabad, India" },
  { firstName: "Zainab", lastName: "Khan", age: 23, dob: "19/05/2001", user_location: "Bangalore, India" },
  { firstName: "Kabir", lastName: "Ansari", age: 25, dob: "06/07/1999", user_location: "Chennai, India" },
  { firstName: "Anaya", lastName: "Fatima", age: 24, dob: "08/02/2000", user_location: "Mangalore, India" },
  { firstName: "Farhan", lastName: "Qureshi", age: 27, dob: "30/10/1997", user_location: "Indore, India" },
  { firstName: "Sana", lastName: "Rehman", age: 22, dob: "01/01/2002", user_location: "Lucknow, India" },

  { firstName: "Mahesh", lastName: "Naidu", age: 28, dob: "07/06/1996", user_location: "Vizag, India" },
  { firstName: "Keerthi", lastName: "Reddy", age: 23, dob: "20/09/2001", user_location: "Hyderabad, India" },
  { firstName: "Arjun", lastName: "Iyer", age: 26, dob: "04/04/1998", user_location: "Chennai, India" },
  { firstName: "Lakshmi", lastName: "Menon", age: 25, dob: "14/12/1999", user_location: "Kochi, India" },
  { firstName: "Vivek", lastName: "Pillai", age: 27, dob: "16/03/1997", user_location: "Trivandrum, India" },
  { firstName: "Anjali", lastName: "Krishnan", age: 24, dob: "09/09/2000", user_location: "Coimbatore, India" },
  { firstName: "Roshan", lastName: "Shetty", age: 26, dob: "19/08/1998", user_location: "Mangalore, India" },
  { firstName: "Meera", lastName: "Pai", age: 22, dob: "12/11/2002", user_location: "Mysore, India" },
  { firstName: "Sandeep", lastName: "Nair", age: 28, dob: "23/07/1996", user_location: "Kollam, India" },
  { firstName: "Priya", lastName: "Warrier", age: 23, dob: "06/05/2001", user_location: "Kozhikode, India" },
  { firstName: "Vikram", lastName: "Singh", age: 27, dob: "12/02/1997", user_location: "Delhi, India" },
  { firstName: "Pallavi", lastName: "Saxena", age: 24, dob: "22/09/2000", user_location: "Kanpur, India" },
  { firstName: "Harshit", lastName: "Chauhan", age: 26, dob: "18/07/1998", user_location: "Bareilly, India" },
  { firstName: "Mahima", lastName: "Verma", age: 25, dob: "09/11/1999", user_location: "Ghaziabad, India" },
  { firstName: "Aayush", lastName: "Gupta", age: 23, dob: "05/10/2001", user_location: "Agra, India" },
  { firstName: "Tanvi", lastName: "Sharma", age: 22, dob: "14/04/2002", user_location: "Meerut, India" },
  { firstName: "Yuvraj", lastName: "Mishra", age: 27, dob: "02/01/1997", user_location: "Prayagraj, India" },
  { firstName: "Kritika", lastName: "Tiwari", age: 25, dob: "29/08/1999", user_location: "Lucknow, India" },
  { firstName: "Raghav", lastName: "Dubey", age: 28, dob: "11/03/1996", user_location: "Noida, India" },
  { firstName: "Aarohi", lastName: "Pandey", age: 24, dob: "30/06/2000", user_location: "Varanasi, India" },

  { firstName: "Dhruv", lastName: "Chaturvedi", age: 26, dob: "16/10/1998", user_location: "Gwalior, India" },
  { firstName: "Saloni", lastName: "Agarwal", age: 22, dob: "02/12/2002", user_location: "Indore, India" },
  { firstName: "Ritesh", lastName: "Bhardwaj", age: 29, dob: "08/05/1995", user_location: "Bhopal, India" },
  { firstName: "Hemangi", lastName: "Bansal", age: 23, dob: "13/04/2001", user_location: "Kota, India" },
  { firstName: "Sparsh", lastName: "Garg", age: 25, dob: "27/09/1999", user_location: "Jaipur, India" },
  { firstName: "Mansi", lastName: "Jain", age: 24, dob: "05/02/2000", user_location: "Udaipur, India" },
  { firstName: "Arnav", lastName: "Suri", age: 26, dob: "07/01/1998", user_location: "Jodhpur, India" },
  { firstName: "Vaishnavi", lastName: "Lodha", age: 23, dob: "24/11/2001", user_location: "Surat, India" },
  { firstName: "Parth", lastName: "Modi", age: 27, dob: "19/08/1997", user_location: "Ahmedabad, India" },
  { firstName: "Trisha", lastName: "Desai", age: 24, dob: "03/03/2000", user_location: "Rajkot, India" },

  { firstName: "Nirav", lastName: "Shah", age: 28, dob: "21/06/1996", user_location: "Vadodara, India" },
  { firstName: "Rhea", lastName: "Kapadia", age: 22, dob: "10/12/2002", user_location: "Mumbai, India" },
  { firstName: "Ayush", lastName: "Thakur", age: 25, dob: "01/04/1999", user_location: "Nashik, India" },
  { firstName: "Samaira", lastName: "Patil", age: 23, dob: "17/05/2001", user_location: "Kolhapur, India" },
  { firstName: "Rudra", lastName: "Kulkarni", age: 27, dob: "26/10/1997", user_location: "Pune, India" },
  { firstName: "Vedika", lastName: "Joshi", age: 24, dob: "06/03/2000", user_location: "Nagpur, India" },
  { firstName: "Hardik", lastName: "Mehta", age: 26, dob: "18/09/1998", user_location: "Mumbai, India" },
  { firstName: "Aishwarya", lastName: "Sawant", age: 23, dob: "12/01/2001", user_location: "Thane, India" },
  { firstName: "Sujal", lastName: "Deshmukh", age: 25, dob: "15/07/1999", user_location: "Akurdi, India" },
  { firstName: "Ritika", lastName: "Lokhande", age: 22, dob: "04/11/2002", user_location: "Solapur, India" },

  { firstName: "Shrey", lastName: "Anand", age: 27, dob: "20/02/1997", user_location: "Hyderabad, India" },
  { firstName: "Anusha", lastName: "Rao", age: 23, dob: "29/09/2001", user_location: "Warangal, India" },
  { firstName: "Karthik", lastName: "Shetty", age: 26, dob: "02/05/1998", user_location: "Bangalore, India" },
  { firstName: "Vaibhavi", lastName: "Pai", age: 25, dob: "11/08/1999", user_location: "Mangalore, India" },
  { firstName: "Roshan", lastName: "Naidu", age: 28, dob: "03/01/1996", user_location: "Chennai, India" },
  { firstName: "Nisha", lastName: "Krishnan", age: 24, dob: "17/06/2000", user_location: "Coimbatore, India" },
  { firstName: "Vignesh", lastName: "Pillai", age: 27, dob: "12/10/1997", user_location: "Trichy, India" },
  { firstName: "Keerthana", lastName: "Menon", age: 22, dob: "01/04/2002", user_location: "Kochi, India" },
  { firstName: "Lokesh", lastName: "Nair", age: 26, dob: "13/07/1998", user_location: "Calicut, India" },
  { firstName: "Aparna", lastName: "Warrier", age: 23, dob: "08/05/2001", user_location: "Trivandrum, India" },

  { firstName: "Bilal", lastName: "Mirza", age: 28, dob: "24/09/1996", user_location: "Srinagar, India" },
  { firstName: "Zoya", lastName: "Nazir", age: 23, dob: "30/12/2001", user_location: "Jammu, India" },
  { firstName: "Rehan", lastName: "Qadri", age: 26, dob: "14/08/1998", user_location: "Delhi, India" },
  { firstName: "Sumbul", lastName: "Alam", age: 25, dob: "05/03/1999", user_location: "Bareilly, India" },
  { firstName: "Faizan", lastName: "Qureshi", age: 27, dob: "19/11/1997", user_location: "Lucknow, India" },
  { firstName: "Areeba", lastName: "Siddiqui", age: 22, dob: "02/02/2002", user_location: "Aligarh, India" },
  { firstName: "Imtiyaz", lastName: "Ansari", age: 29, dob: "28/04/1995", user_location: "Patna, India" },
  { firstName: "Maryam", lastName: "Khan", age: 24, dob: "07/07/2000", user_location: "Ranchi, India" },
  { firstName: "Danish", lastName: "Sheikh", age: 26, dob: "21/10/1998", user_location: "Bhopal, India" },
  { firstName: "Nafisa", lastName: "Saiyed", age: 23, dob: "15/05/2001", user_location: "Surat, India" },
  { firstName: "Harsh", lastName: "Tiwari", age: 26, dob: "14/03/1998", user_location: "Kanpur, India" },
  { firstName: "Ritika", lastName: "Mishra", age: 23, dob: "21/07/2001", user_location: "Delhi, India" },
  { firstName: "Gaurav", lastName: "Sharma", age: 27, dob: "03/11/1997", user_location: "Indore, India" },
  { firstName: "Kavita", lastName: "Yadav", age: 22, dob: "16/05/2002", user_location: "Bhopal, India" },
  { firstName: "Akshay", lastName: "Verma", age: 28, dob: "09/12/1996", user_location: "Jaipur, India" },
  { firstName: "Manisha", lastName: "Gupta", age: 24, dob: "01/04/2000", user_location: "Gurgaon, India" },
  { firstName: "Harinder", lastName: "Kaur", age: 23, dob: "08/09/2001", user_location: "Ludhiana, India" },
  { firstName: "Yogesh", lastName: "Rana", age: 29, dob: "25/01/1995", user_location: "Noida, India" },
  { firstName: "Sneha", lastName: "Prajapati", age: 21, dob: "11/06/2003", user_location: "Varanasi, India" },
  { firstName: "Deepak", lastName: "Saxena", age: 30, dob: "19/02/1994", user_location: "Agra, India" },

  { firstName: "Vikram", lastName: "Saini", age: 27, dob: "06/10/1997", user_location: "Shimla, India" },
  { firstName: "Pallavi", lastName: "Jain", age: 22, dob: "12/12/2002", user_location: "Udaipur, India" },
  { firstName: "Umesh", lastName: "Rawat", age: 25, dob: "27/11/1999", user_location: "Surat, India" },
  { firstName: "Tanya", lastName: "Kapoor", age: 23, dob: "17/05/2001", user_location: "Delhi, India" },
  { firstName: "Sahil", lastName: "Khan", age: 26, dob: "03/08/1998", user_location: "Mumbai, India" },
  { firstName: "Nisha", lastName: "Rajput", age: 24, dob: "22/01/2000", user_location: "Bhopal, India" },
  { firstName: "Amit", lastName: "Tripathi", age: 29, dob: "09/04/1995", user_location: "Kanpur, India" },
  { firstName: "Rekha", lastName: "Seth", age: 28, dob: "13/03/1996", user_location: "Pune, India" },
  { firstName: "Jay", lastName: "Patel", age: 27, dob: "30/06/1997", user_location: "Ahmedabad, India" },
  { firstName: "Isha", lastName: "Mehta", age: 23, dob: "28/07/2001", user_location: "Rajkot, India" },

  { firstName: "Rohan", lastName: "Chauhan", age: 26, dob: "18/02/1998", user_location: "Dehradun, India" },
  { firstName: "Kritika", lastName: "Singh", age: 22, dob: "05/05/2002", user_location: "Lucknow, India" },
  { firstName: "Abhinav", lastName: "Mishra", age: 28, dob: "12/09/1996", user_location: "Gorakhpur, India" },
  { firstName: "Tanvi", lastName: "Saxena", age: 24, dob: "09/11/2000", user_location: "Agra, India" },
  { firstName: "Vivek", lastName: "Jaiswal", age: 25, dob: "14/01/1999", user_location: "Mirzapur, India" },
  { firstName: "Meera", lastName: "Gupta", age: 23, dob: "07/08/2001", user_location: "Kanpur, India" },
  { firstName: "Arjun", lastName: "Rathore", age: 29, dob: "16/10/1995", user_location: "Jodhpur, India" },
  { firstName: "Lavanya", lastName: "Kumari", age: 21, dob: "18/12/2003", user_location: "Patna, India" },
  { firstName: "Ritesh", lastName: "Tomar", age: 27, dob: "02/03/1997", user_location: "Gwalior, India" },
  { firstName: "Payal", lastName: "Agrawal", age: 24, dob: "11/04/2000", user_location: "Indore, India" },

  { firstName: "Shreyas", lastName: "Gokhale", age: 28, dob: "06/02/1996", user_location: "Nagpur, India" },
  { firstName: "Damini", lastName: "Kulkarni", age: 23, dob: "09/09/2001", user_location: "Pune, India" },
  { firstName: "Sagar", lastName: "Pande", age: 27, dob: "01/01/1997", user_location: "Nashik, India" },
  { firstName: "Muskan", lastName: "Shetty", age: 22, dob: "25/05/2002", user_location: "Mangalore, India" },
  { firstName: "Rudra", lastName: "Iyer", age: 28, dob: "14/06/1996", user_location: "Chennai, India" },
  { firstName: "Preeti", lastName: "Chhabra", age: 25, dob: "07/10/1999", user_location: "Delhi, India" },
  { firstName: "Dev", lastName: "Bhardwaj", age: 29, dob: "19/07/1995", user_location: "Ambala, India" },
  { firstName: "Sonia", lastName: "Lamba", age: 23, dob: "12/03/2001", user_location: "Panipat, India" },
  { firstName: "Madhav", lastName: "Puri", age: 26, dob: "03/11/1998", user_location: "Haridwar, India" },
  { firstName: "Juhi", lastName: "Saxena", age: 24, dob: "29/09/2000", user_location: "Bareilly, India" },

  { firstName: "Kabir", lastName: "Malhotra", age: 27, dob: "17/02/1997", user_location: "Delhi, India" },
  { firstName: "Ananya", lastName: "Saini", age: 22, dob: "23/08/2002", user_location: "Sonipat, India" },
  { firstName: "Ravindra", lastName: "Kesari", age: 30, dob: "10/05/1994", user_location: "Kanpur, India" },
  { firstName: "Kajal", lastName: "Parmar", age: 24, dob: "02/06/2000", user_location: "Vadodara, India" },
  { firstName: "Pranay", lastName: "Garg", age: 26, dob: "03/01/1998", user_location: "Delhi, India" },
  { firstName: "Surbhi", lastName: "Dixit", age: 23, dob: "21/07/2001", user_location: "Kanpur, India" },
  { firstName: "Aditya", lastName: "Sharma", age: 28, dob: "05/05/1996", user_location: "Meerut, India" },
  { firstName: "Monika", lastName: "Bansal", age: 25, dob: "11/11/1999", user_location: "Kota, India" },
  { firstName: "Raghav", lastName: "Solanki", age: 27, dob: "18/09/1997", user_location: "Vadodara, India" },
  { firstName: "Divya", lastName: "Chawla", age: 24, dob: "20/10/2000", user_location: "Surat, India" },
  { firstName: "Bilal", lastName: "Mirza", age: 28, dob: "24/09/1996", user_location: "Srinagar, India" },
  { firstName: "Zoya", lastName: "Nazir", age: 23, dob: "30/12/2001", user_location: "Jammu, India" },
  { firstName: "Rehan", lastName: "Qadri", age: 26, dob: "14/08/1998", user_location: "Delhi, India" },
  { firstName: "Sumbul", lastName: "Alam", age: 25, dob: "05/03/1999", user_location: "Bareilly, India" },
  { firstName: "Faizan", lastName: "Qureshi", age: 27, dob: "19/11/1997", user_location: "Lucknow, India" },
  { firstName: "Areeba", lastName: "Siddiqui", age: 22, dob: "02/02/2002", user_location: "Aligarh, India" },
  { firstName: "Imtiyaz", lastName: "Ansari", age: 29, dob: "28/04/1995", user_location: "Patna, India" },
  { firstName: "Maryam", lastName: "Khan", age: 24, dob: "07/07/2000", user_location: "Ranchi, India" },
  { firstName: "Bilal", lastName: "Mirza", age: 28, dob: "24/09/1996", user_location: "Srinagar, India" },
  { firstName: "Zoya", lastName: "Nazir", age: 23, dob: "30/12/2001", user_location: "Jammu, India" },
  { firstName: "Rehan", lastName: "Qadri", age: 26, dob: "14/08/1998", user_location: "Delhi, India" },
  { firstName: "Sumbul", lastName: "Alam", age: 25, dob: "05/03/1999", user_location: "Bareilly, India" },
  { firstName: "Faizan", lastName: "Qureshi", age: 27, dob: "19/11/1997", user_location: "Lucknow, India" },
  { firstName: "Areeba", lastName: "Siddiqui", age: 22, dob: "02/02/2002", user_location: "Aligarh, India" },
  { firstName: "Imtiyaz", lastName: "Ansari", age: 29, dob: "28/04/1995", user_location: "Patna, India" },
  { firstName: "Maryam", lastName: "Khan", age: 24, dob: "07/07/2000", user_location: "Ranchi, India" },
  { firstName: "Bilal", lastName: "Mirza", age: 28, dob: "24/09/1996", user_location: "Srinagar, India" },
  { firstName: "Zoya", lastName: "Nazir", age: 23, dob: "30/12/2001", user_location: "Jammu, India" },
  { firstName: "Rehan", lastName: "Qadri", age: 26, dob: "14/08/1998", user_location: "Delhi, India" },
  { firstName: "Sumbul", lastName: "Alam", age: 25, dob: "05/03/1999", user_location: "Bareilly, India" },
  { firstName: "Faizan", lastName: "Qureshi", age: 27, dob: "19/11/1997", user_location: "Lucknow, India" },
  { firstName: "Areeba", lastName: "Siddiqui", age: 22, dob: "02/02/2002", user_location: "Aligarh, India" },
  { firstName: "Imtiyaz", lastName: "Ansari", age: 29, dob: "28/04/1995", user_location: "Patna, India" },
  { firstName: "Maryam", lastName: "Khan", age: 24, dob: "07/07/2000", user_location: "Ranchi, India" },
  { firstName: "Bilal", lastName: "Mirza", age: 28, dob: "24/09/1996", user_location: "Srinagar, India" },
  { firstName: "Zoya", lastName: "Nazir", age: 23, dob: "30/12/2001", user_location: "Jammu, India" },
  { firstName: "Rehan", lastName: "Qadri", age: 26, dob: "14/08/1998", user_location: "Delhi, India" },
  { firstName: "Sumbul", lastName: "Alam", age: 25, dob: "05/03/1999", user_location: "Bareilly, India" },
  { firstName: "Faizan", lastName: "Qureshi", age: 27, dob: "19/11/1997", user_location: "Lucknow, India" },
  { firstName: "Areeba", lastName: "Siddiqui", age: 22, dob: "02/02/2002", user_location: "Aligarh, India" },
  { firstName: "Imtiyaz", lastName: "Ansari", age: 29, dob: "28/04/1995", user_location: "Patna, India" },
  { firstName: "Maryam", lastName: "Khan", age: 24, dob: "07/07/2000", user_location: "Ranchi, India" },
  { firstName: "Bilal", lastName: "Mirza", age: 28, dob: "24/09/1996", user_location: "Srinagar, India" },
  { firstName: "Zoya", lastName: "Nazir", age: 23, dob: "30/12/2001", user_location: "Jammu, India" },
  { firstName: "Rehan", lastName: "Qadri", age: 26, dob: "14/08/1998", user_location: "Delhi, India" },
  { firstName: "Sumbul", lastName: "Alam", age: 25, dob: "05/03/1999", user_location: "Bareilly, India" },
  { firstName: "Faizan", lastName: "Qureshi", age: 27, dob: "19/11/1997", user_location: "Lucknow, India" },
  { firstName: "Areeba", lastName: "Siddiqui", age: 22, dob: "02/02/2002", user_location: "Aligarh, India" },
  { firstName: "Imtiyaz", lastName: "Ansari", age: 29, dob: "28/04/1995", user_location: "Patna, India" },
  { firstName: "Maryam", lastName: "Khan", age: 24, dob: "07/07/2000", user_location: "Ranchi, India" },
  { firstName: "Bilal", lastName: "Mirza", age: 28, dob: "24/09/1996", user_location: "Srinagar, India" },
  { firstName: "Zoya", lastName: "Nazir", age: 23, dob: "30/12/2001", user_location: "Jammu, India" },
  { firstName: "Rehan", lastName: "Qadri", age: 26, dob: "14/08/1998", user_location: "Delhi, India" },
  { firstName: "Sumbul", lastName: "Alam", age: 25, dob: "05/03/1999", user_location: "Bareilly, India" },
  { firstName: "Faizan", lastName: "Qureshi", age: 27, dob: "19/11/1997", user_location: "Lucknow, India" },
  { firstName: "Areeba", lastName: "Siddiqui", age: 22, dob: "02/02/2002", user_location: "Aligarh, India" },
  { firstName: "Imtiyaz", lastName: "Ansari", age: 29, dob: "28/04/1995", user_location: "Patna, India" },
  { firstName: "Maryam", lastName: "Khan", age: 24, dob: "07/07/2000", user_location: "Ranchi, India" },
  { firstName: "Bilal", lastName: "Mirza", age: 28, dob: "24/09/1996", user_location: "Srinagar, India" },
  { firstName: "Zoya", lastName: "Nazir", age: 23, dob: "30/12/2001", user_location: "Jammu, India" },
  { firstName: "Rehan", lastName: "Qadri", age: 26, dob: "14/08/1998", user_location: "Delhi, India" },
  { firstName: "Sumbul", lastName: "Alam", age: 25, dob: "05/03/1999", user_location: "Bareilly, India" },
  { firstName: "Faizan", lastName: "Qureshi", age: 27, dob: "19/11/1997", user_location: "Lucknow, India" },
  { firstName: "Areeba", lastName: "Siddiqui", age: 22, dob: "02/02/2002", user_location: "Aligarh, India" },
  { firstName: "Imtiyaz", lastName: "Ansari", age: 29, dob: "28/04/1995", user_location: "Patna, India" },
  { firstName: "Maryam", lastName: "Khan", age: 24, dob: "07/07/2000", user_location: "Ranchi, India" },
  { firstName: "Bilal", lastName: "Mirza", age: 28, dob: "24/09/1996", user_location: "Srinagar, India" },
  { firstName: "Zoya", lastName: "Nazir", age: 23, dob: "30/12/2001", user_location: "Jammu, India" },
  { firstName: "Rehan", lastName: "Qadri", age: 26, dob: "14/08/1998", user_location: "Delhi, India" },
  { firstName: "Sumbul", lastName: "Alam", age: 25, dob: "05/03/1999", user_location: "Bareilly, India" },
  { firstName: "Faizan", lastName: "Qureshi", age: 27, dob: "19/11/1997", user_location: "Lucknow, India" },
  { firstName: "Areeba", lastName: "Siddiqui", age: 22, dob: "02/02/2002", user_location: "Aligarh, India" },
  { firstName: "Imtiyaz", lastName: "Ansari", age: 29, dob: "28/04/1995", user_location: "Patna, India" },
  { firstName: "Maryam", lastName: "Khan", age: 24, dob: "07/07/2000", user_location: "Ranchi, India" },
  { firstName: "Bilal", lastName: "Mirza", age: 28, dob: "24/09/1996", user_location: "Srinagar, India" },
  { firstName: "Zoya", lastName: "Nazir", age: 23, dob: "30/12/2001", user_location: "Jammu, India" },
  { firstName: "Rehan", lastName: "Qadri", age: 26, dob: "14/08/1998", user_location: "Delhi, India" },
  { firstName: "Sumbul", lastName: "Alam", age: 25, dob: "05/03/1999", user_location: "Bareilly, India" },
  { firstName: "Faizan", lastName: "Qureshi", age: 27, dob: "19/11/1997", user_location: "Lucknow, India" },
  { firstName: "Areeba", lastName: "Siddiqui", age: 22, dob: "02/02/2002", user_location: "Aligarh, India" },
  { firstName: "Imtiyaz", lastName: "Ansari", age: 29, dob: "28/04/1995", user_location: "Patna, India" },
  { firstName: "Maryam", lastName: "Khan", age: 24, dob: "07/07/2000", user_location: "Ranchi, India" },
  { firstName: "Bilal", lastName: "Mirza", age: 28, dob: "24/09/1996", user_location: "Srinagar, India" },
  { firstName: "Zoya", lastName: "Nazir", age: 23, dob: "30/12/2001", user_location: "Jammu, India" },
  { firstName: "Rehan", lastName: "Qadri", age: 26, dob: "14/08/1998", user_location: "Delhi, India" },
  { firstName: "Sumbul", lastName: "Alam", age: 25, dob: "05/03/1999", user_location: "Bareilly, India" },
  { firstName: "Faizan", lastName: "Qureshi", age: 27, dob: "19/11/1997", user_location: "Lucknow, India" },
  { firstName: "Areeba", lastName: "Siddiqui", age: 22, dob: "02/02/2002", user_location: "Aligarh, India" },
  { firstName: "Imtiyaz", lastName: "Ansari", age: 29, dob: "28/04/1995", user_location: "Patna, India" },
  { firstName: "Maryam", lastName: "Khan", age: 24, dob: "07/07/2000", user_location: "Ranchi, India" },
  { firstName: "Bilal", lastName: "Mirza", age: 28, dob: "24/09/1996", user_location: "Srinagar, India" },
  { firstName: "Zoya", lastName: "Nazir", age: 23, dob: "30/12/2001", user_location: "Jammu, India" },
  { firstName: "Rehan", lastName: "Qadri", age: 26, dob: "14/08/1998", user_location: "Delhi, India" },
  { firstName: "Sumbul", lastName: "Alam", age: 25, dob: "05/03/1999", user_location: "Bareilly, India" },
  { firstName: "Faizan", lastName: "Qureshi", age: 27, dob: "19/11/1997", user_location: "Lucknow, India" },
  { firstName: "Areeba", lastName: "Siddiqui", age: 22, dob: "02/02/2002", user_location: "Aligarh, India" },
  { firstName: "Imtiyaz", lastName: "Ansari", age: 29, dob: "28/04/1995", user_location: "Patna, India" },
  { firstName: "Maryam", lastName: "Khan", age: 24, dob: "07/07/2000", user_location: "Ranchi, India" },
  { firstName: "Bilal", lastName: "Mirza", age: 28, dob: "24/09/1996", user_location: "Srinagar, India" },
  { firstName: "Zoya", lastName: "Nazir", age: 23, dob: "30/12/2001", user_location: "Jammu, India" },
  { firstName: "Rehan", lastName: "Qadri", age: 26, dob: "14/08/1998", user_location: "Delhi, India" },
  { firstName: "Sumbul", lastName: "Alam", age: 25, dob: "05/03/1999", user_location: "Bareilly, India" },
  { firstName: "Faizan", lastName: "Qureshi", age: 27, dob: "19/11/1997", user_location: "Lucknow, India" },
  { firstName: "Areeba", lastName: "Siddiqui", age: 22, dob: "02/02/2002", user_location: "Aligarh, India" },
  { firstName: "Imtiyaz", lastName: "Ansari", age: 29, dob: "28/04/1995", user_location: "Patna, India" },
  { firstName: "Maryam", lastName: "Khan", age: 24, dob: "07/07/2000", user_location: "Ranchi, India" },
  { firstName: "Bilal", lastName: "Mirza", age: 28, dob: "24/09/1996", user_location: "Srinagar, India" },
  { firstName: "Zoya", lastName: "Nazir", age: 23, dob: "30/12/2001", user_location: "Jammu, India" },
  { firstName: "Rehan", lastName: "Qadri", age: 26, dob: "14/08/1998", user_location: "Delhi, India" },
  { firstName: "Sumbul", lastName: "Alam", age: 25, dob: "05/03/1999", user_location: "Bareilly, India" },
  { firstName: "Faizan", lastName: "Qureshi", age: 27, dob: "19/11/1997", user_location: "Lucknow, India" },
  { firstName: "Areeba", lastName: "Siddiqui", age: 22, dob: "02/02/2002", user_location: "Aligarh, India" },
  { firstName: "Imtiyaz", lastName: "Ansari", age: 29, dob: "28/04/1995", user_location: "Patna, India" },
  { firstName: "Maryam", lastName: "Khan", age: 24, dob: "07/07/2000", user_location: "Ranchi, India" },
];

// ----------------------
// Generate Mock FB Users (with friends + follower count)
// ----------------------
function generateMockUsers() {
  let currentIdNumber = BigInt(fbBaseId);

  fbNames.forEach((user, index) => {
    const userId = (currentIdNumber + BigInt(index)).toString();

    const followers = Math.floor(Math.random() * 5000) + 500; // 500–5500
    const friendsCount = Math.floor(Math.random() * 30) + 5; // 5–35

    // generate random friends list
    const friends = [];
    while (friends.length < friendsCount) {
      const randomIndex = Math.floor(Math.random() * fbNames.length);
      if (randomIndex !== index && !friends.includes(randomIndex)) {
        friends.push(randomIndex);
      }
    }

    const userData = {
      id: userId,
      name: `${user.firstName} ${user.lastName}`,
      first_name: user.firstName,
      last_name: user.lastName,
      age: user.age,
      dob: user.dob,
      user_location: user.user_location,
      followers: followers,
      friends: friends.map(i => ({
        id: (currentIdNumber + BigInt(i)).toString(),
        name: `${fbNames[i].firstName} ${fbNames[i].lastName}`
      }))
    };

    fbUsers.push(userData);
    fbUserMap[userId] = userData;
  });

  console.log("Mock FB Users Generated:", fbUsers.length);
}

generateMockUsers();



// Add FB users safely using BigInt
fbNames.forEach((user, i) => {
  const id = (BigInt(fbBaseId) + BigInt(i)).toString();
  fbUsers.push({ ...user, id, friends: [] });
  fbUserMap[id] = fbUsers[i];
});

// Assign friends: each user has next 5 users cyclically
const fbIds = Object.keys(fbUserMap);
fbIds.forEach((id, i) => {
  fbUserMap[id].friends = fbIds
    .slice(i + 1, i + 6)
    .map(fid => ({ id: fid, firstName: fbUserMap[fid].firstName, lastName: fbUserMap[fid].lastName }));
});

// ----------------------
// Dummy IG Users (20 users with followers and location)
// ----------------------
const igBaseId = "133094043977116573"; // string
const igUsers = {};
fbNames.forEach((user, i) => {
  const id = (BigInt(igBaseId) + BigInt(i)).toString();
  igUsers[id] = { ...user, id, followers: [] }; // user_location included
});

// Assign followers: each user has next 5 users cyclically
const igIds = Object.keys(igUsers);
igIds.forEach((id, i) => {
  igUsers[id].followers = igIds
    .slice(i + 1, i + 359)
    .map(fid => ({
      id: fid,
      username: igUsers[fid].firstName.toLowerCase() + "_" + igUsers[fid].lastName.toLowerCase()
    }));
});

// ----------------------
// Helper: validate token
// ----------------------
function checkToken(req) {
  const token = req.query.token || req.headers["x-access-token"];
  if (!token) return { ok: false, code: 401, msg: "Token missing" };
  if (!validTokens.has(token)) return { ok: false, code: 403, msg: "Invalid token" };
  return { ok: true, token };
}

// ----------------------
// Health Check
// ----------------------
app.get("/", (req, res) => {
  res.json({ ok: true, message: "Mock Social Server Running..." });
});

// ----------------------
// FACEBOOK API
// ----------------------
app.get("/fb/:id", (req, res) => {
  const { id } = req.params;
  const check = checkToken(req);
  if (!check.ok) return res.status(check.code).json({ error: check.msg });

  const user = fbUserMap[id];
  if (!user) return res.status(404).json({ error: "Facebook user not found" });

  res.json({
    id: user.id,
    firstName: user.firstName,
    lastName: user.lastName,
    age: user.age,
    dob: user.dob || null,
    user_location: user.user_location,
    friends: user.friends,
    totalFriends: user.friends.length
  });
});

// ----------------------
// INSTAGRAM API
// ----------------------
app.get("/ig/:id", (req, res) => {
  const { id } = req.params;
  const check = checkToken(req);
  if (!check.ok) return res.status(check.code).json({ error: check.msg });

  const user = igUsers[id];
  if (!user) return res.status(404).json({ error: "Instagram user not found" });

  res.json({
    id: user.id,
    firstName: user.firstName,
    lastName: user.lastName,
    user_location: user.user_location,
     totalFollowers: user.followers.length,
    // totalFollowers: 358,

    followers: user.followers
  });
});

// ----------------------
// List of Valid Tokens
// ----------------------
app.get("/__tokens", (req, res) => {
  res.json({ validTokens: Array.from(validTokens) });
});

// ----------------------
// Add Token at Runtime
// ----------------------
app.post("/add-token", (req, res) => {
  const body = req.body;
  if (!body || !body.token) return res.status(400).json({ error: "Provide token in body" });
  validTokens.add(body.token.trim());
  res.json({ success: true, tokens: Array.from(validTokens) });
});

// ----------------------
// Start server
// ----------------------
app.listen(PORT, () => {
  console.log(`🚀 Mock Social Server running at http://localhost:${PORT}`);
});
