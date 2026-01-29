const bouton=document.querySelector(".bouton");
const fenetre=document.getElementById("fenetre");
const yes=document.getElementById("yes");
const no=document.getElementById("no");
const close=document.getElementById("close");
const openbtn=document.querySelector(".openbtn")
const closen=document.querySelector(".closen")
const navbar=document.getElementById("navbar")
const dabou=document.getElementById("dabou")
const contact=document.getElementById("contact")


bouton.addEventListener("click",()=>{
    fenetre.style.display="flex";
    openbtn.style.display="none";
    navbar.style.display="none"
     dabou.style.display="none"
});
no.addEventListener("click",()=>{
    fenetre.style.display="none";
    openbtn.style.display="flex"; 
     navbar.style.display="flex"
      dabou.style.display="flex"
       navbar.style.display="none";
});
close.addEventListener("click",()=>{
    fenetre.style.display="none";
      openbtn.style.display="flex"; 
       dabou.style.display="flex"
})
yes.addEventListener("click",()=>{
    alert("DABOU SAMSON FOREVER!")
})
closen.addEventListener("click",()=>{
    navbar.style.display="none";
    openbtn.style.display="flex";
    dabou.style.display="flex"
})
dabou.addEventListener("click",()=>{
  navbar.style.display="flex"
  dabou.style.display="none"

})