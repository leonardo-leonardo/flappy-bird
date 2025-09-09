import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Rolling Bird", page_icon="🎮", layout="centered")
st.title("🎮 Rolling Bird Game")

flappy_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
body { margin: 0; overflow: hidden; }
canvas { display: block; margin: 0 auto; }
</style>
</head>
<body>
<canvas id="gameCanvas" width="400" height="600"></canvas>
<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let frames = 0;
const DEGREE = Math.PI/180;

// Game state
const state = { current: 0, getReady: 0, game: 1, over: 2 };

// Score & Level
let score = 0;
let level = 1;

// Control the game
canvas.addEventListener("click", function(evt){
    switch(state.current){
        case state.getReady: state.current = state.game; break;
        case state.game: bird.flap(); break;
        case state.over: state.current = state.getReady; pipes.reset(); bird.reset(); score=0; level=1; break;
    }
});

// Bird
const bird = {
    x: 50,
    y: 150,
    radius: 12,
    gravity: 0.015,
    jump: 0.92,
    speed: 0,
    rotation: 0,
    wing: 0,
    
    draw: function(){
        ctx.save();
        ctx.translate(this.x, this.y);
        ctx.rotate(this.rotation);
        
        // Body
        ctx.fillStyle = "yellow";
        ctx.beginPath();
        ctx.ellipse(0, 0, this.radius*1.2, this.radius, 0, 0, Math.PI*2);
        ctx.fill();
        
        // Wing
        ctx.fillStyle = "orange";
        let wingOffset = Math.sin(this.wing)*6;
        ctx.beginPath();
        ctx.ellipse(-3, wingOffset, 5, 2, Math.PI/4, 0, Math.PI*2);
        ctx.fill();
        
        // Eye
        ctx.fillStyle = "black";
        ctx.beginPath();
        ctx.arc(4, -3, 2, 0, Math.PI*2);
        ctx.fill();
        
        // Beak
        ctx.fillStyle = "red";
        ctx.beginPath();
        ctx.moveTo(this.radius*1.2, 0);
        ctx.lineTo(this.radius*1.2+6, -3);
        ctx.lineTo(this.radius*1.2+6, 3);
        ctx.closePath();
        ctx.fill();
        
        ctx.restore();
    },
    
    flap: function(){ this.speed = -this.jump; },
    
    update: function(){
        this.speed += this.gravity;
        this.y += this.speed;
        this.rotation += (this.speed >= this.jump ? 0.05 : -0.1);
        if(this.y + this.radius >= canvas.height){
            this.y = canvas.height - this.radius;
            if(state.current == state.game) state.current = state.over;
        }
        this.wing += 0.3;
    },
    
    reset: function(){ this.y = 150; this.speed = 0; this.rotation = 0; this.wing = 0; }
};

// Pipes
const pipes = {
    position: [],
    width: 50,
    height: 400,
    gap: 400,
    dx: 2,
    radius: 10,  // round corner radius
    
    drawPipe: function(x, y, w, h){
        ctx.fillStyle = "green";
        ctx.beginPath();
        ctx.moveTo(x + this.radius, y);
        ctx.lineTo(x + w - this.radius, y);
        ctx.quadraticCurveTo(x + w, y, x + w, y + this.radius);
        ctx.lineTo(x + w, y + h - this.radius);
        ctx.quadraticCurveTo(x + w, y + h, x + w - this.radius, y + h);
        ctx.lineTo(x + this.radius, y + h);
        ctx.quadraticCurveTo(x, y + h, x, y + h - this.radius);
        ctx.lineTo(x, y + this.radius);
        ctx.quadraticCurveTo(x, y, x + this.radius, y);
        ctx.fill();
    },
    
    draw: function(){
        for(let p of this.position){
            this.drawPipe(p.x, p.y, this.width, this.height);
            this.drawPipe(p.x, p.y + this.height + this.gap, this.width, this.height);
        }
    },
    
    update: function(){
        if(state.current !== state.game) return;
        if(frames % 100 === 0){
            let top = Math.random() * (canvas.height/2);
            this.position.push({x: canvas.width, y: top - this.height});
        }
        for(let i=0; i<this.position.length; i++){
            let p = this.position[i];
            p.x -= this.dx;
            
            if(p.x + this.width/2 < bird.x && !p.passed){
                p.passed = true;
                score++;
                level = Math.min(10, Math.floor(score/30)+1);
            }
            
            if(bird.x + bird.radius > p.x && bird.x - bird.radius < p.x + this.width &&
               (bird.y + bird.radius > p.y && bird.y - bird.radius < p.y + this.height ||
                bird.y + bird.radius > p.y + this.height + this.gap && bird.y - bird.radius < p.y + this.height + this.gap + this.height)){
                state.current = state.over;
            }
            
            if(p.x + this.width <= 0) this.position.shift();
        }
    },
    
    reset: function(){ this.position = []; }
};

// Draw background
function drawBackground(){
    // Sky gradient
    let grd = ctx.createLinearGradient(0,0,0,canvas.height);
    grd.addColorStop(0, "#70c5ce");
    grd.addColorStop(1, "#87CEFA");
    ctx.fillStyle = grd;
    ctx.fillRect(0,0,canvas.width,canvas.height);
    
    // Ground
    ctx.fillStyle = "#ded895";
    ctx.fillRect(0, canvas.height - 40, canvas.width, 40);
}

// Draw score & level
function drawScore(){
    ctx.fillStyle = "white";
    ctx.font = "25px Arial";
    ctx.fillText("Score: " + score, 10, 40);
    ctx.fillText("Level: " + level, 10, 70);
}

// Draw & update
function draw(){ 
    drawBackground();
    pipes.draw(); 
    bird.draw(); 
    drawScore();
}

function update(){ 
    bird.update(); 
    pipes.update(); 
}

// Game loop
function loop(){ 
    update(); 
    draw(); 
    frames++; 
    requestAnimationFrame(loop); 
}

loop();
</script>
</body>
</html>
"""

components.html(flappy_html, height=650)
