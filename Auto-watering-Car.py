#include <Servo.h> 
int motorL1=6; //定义左边轮子前进方向 
int motorL2=5; //定义左边轮子后退方向 
int motorR1=9; //定义右边轮子前进方向 
int motorR2=11; //定义右边轮子后退方向 
int water_machine=13; //定义水泵使能管脚 
int water_testPin=A4; //定义土壤湿度输入管脚 
int water_test=0; //定义土壤湿度全局变量 
int water_level=512; //定义土壤湿度判定值 
int temP=12; //定义温度输入管脚 
int box_level=A5; //定义储水槽水位输入管脚 
int box=0; //定义储水槽水位全局变量 
Servo s; //超声波转向舵机 
int trig_f=4; //发射信号（前部测距） 
int echo_f=2; //接收信号（前部测距） 
int trig_b=3; //发射信号（后部测距） 
int echo_b=7; //接收信号（后部测距） 
int level=250;//光阈值 
unsigned int S_l; //距离存储（前左） 
unsigned int S_r; //距离存储（前右） 
unsigned int S_m; //距离存储（前中） 
unsigned int S_b; //距离存储（后） 
 
int sensorPin_fl= A0;    // 定义光传感器（左前）模拟输入管脚 
int sensorValue_fl= 0;  // 定义光传感器（左前）模拟输入全局变量 
int sensorPin_fr= A1;    //定义光传感器（右前）模拟输入管脚 
int sensorValue_fr= 0;  // 定义光传感器（右前）模拟输入全局变量 
int sensorPin_bl= A2;    // 定义光传感器（左后）模拟输入管脚 
int sensorValue_bl= 0;  // 定义光传感器（左后）模拟输入全局变量 
int sensorPin_br= A3;    //定义光传感器（右后）模拟输入管脚 
int sensorValue_br= 0;  // 定义光传感器（右后）模拟输入全局变量 
 
void setup() 
{ 
Serial.begin(9600); //设置波特率 
pinMode(trig_f,OUTPUT); //设置引脚模式 
pinMode(echo_f,INPUT); //设置引脚模式 
pinMode(trig_b,OUTPUT); //设置引脚模式 
pinMode(echo_b,INPUT); //设置引脚模式 
pinMode(motorL1,OUTPUT); 
pinMode(motorL2,OUTPUT); 
pinMode(motorR1,OUTPUT); 
pinMode(motorR2,OUTPUT); 
pinMode(sensorPin_fl,INPUT); 
pinMode(sensorPin_fr,INPUT); 
pinMode(sensorPin_bl,INPUT); 
pinMode(sensorPin_br,INPUT);
pinMode(water_machine,OUTPUT); 
pinMode(water_test,INPUT); 
pinMode(temP,INPUT); 
pinMode(box_level,INPUT); 
 
//pinMode(12,OUTPUT); 
s.attach(8); //定义舵机所用引脚 
s.write(90); //初始化舵机角度 
tone(12,800,500); 
delay(2000); //开机延时 
} 
 
 
void loop() //主函数
{
// read the value from the sensor:   
sensorValue_fl = analogRead(sensorPin_fl);   
Serial.print("sensorValue_fl = ");  //串口输出"Intensity = "   
Serial.println(sensorValue_fl); 
//向串口发送 sensorValue_fl 的值，可以在显示器上显示光强值   
sensorValue_fr = analogRead(sensorPin_fr);   
Serial.print("sensorValue_fr = ");  //串口输出" sensorValue_fr = " 
 
Serial.println(sensorValue_fr);   
sensorValue_bl = analogRead(sensorPin_bl);   
Serial.print("sensorValue_bl = ");     
Serial.println(sensorValue_bl);     
sensorValue_br = analogRead(sensorPin_br);   
Serial.print("sensorValue_br = ");      
Serial.println(sensorValue_br);        
water_test = analogRead(water_testPin);   
Serial.print("water_test = ");   //输出土壤湿度值   
Serial.println(water_test);    
int temP_level = digitalRead(12);   
box = analogRead(box_level);   
Serial.print("box_level = ");   //输出水箱储水值 
 
Serial.println(box);     
delay(500);      
// stop the program for <sensorValue> milliseconds:   
//delay(sensorValue_fl);   
//delay(sensorValue_fr);   
//delay(sensorValue_bl);   
//delay(sensorValue_br); 
 
 
// 
//下面的 XXXX 分别代表小车四个角的光传感器判定的亮暗 
//如 1010 代表小车左前和左后光照更强，小车执行左转指令 
//如 0001 代表小车右后光照更强，小车执行左转指令后再判断执行后退指令 
//   
if(temP_level==HIGH)
	{      
	if(sensorValue_fl<506 && sensorValue_fr<506 && sensorValue_bl<506 && sensorValue_br<506)
		{            
		if(sensorValue_fl<level && sensorValue_fr>level && sensorValue_bl>level && sensorValue_br>level)    //1000               
			{range_f(); //执行测距函数                 
			if(S_l>30 && S_m>30)                    
			L();                  
			}            
		else if(sensorValue_fl>level && sensorValue_fr<level && sensorValue_bl>level && sensorValue_br>level)//0100                
			{range_f(); //执行测距函数                 
			if(S_r>30 && S_m>30)                    
			R(); 
            }            
		else if(sensorValue_fl>level && sensorValue_fr>level && sensorValue_bl<level && sensorValue_br>level)//0010               
			{range_b(); //执行测距函数                 
			if(S_b>30)                   
			{R();
			}                  
			}            
		else if(sensorValue_fl>level && sensorValue_fr>level && sensorValue_bl>level && sensorValue_br<level)//0001                
			{range_b(); //执行测距函数                 
			if(S_b>30)                   
			{L();}                  
			}            
		else if(sensorValue_fl<level && sensorValue_fr<level && sensorValue_bl>level && sensorValue_br>level)//1100                
			{range_f(); //执行测距函数                 
			if(S_r>30 && S_m>30 && S_l>30)                    
				line();                  
			}            
		else if(sensorValue_fl<level && sensorValue_fr>level && sensorValue_bl<level && sensorValue_br>level)//1010                
			{range_f(); //执行测距函数                 
			if(S_l>30 && S_m>30)                    
				{L();}                  
			}            
		//    else if(sensorValue_fl<level && sensorValue_fr>level && sensorValue_bl>level && sensorValue_br<level){}  1001            
		//    else if(sensorValue_fl>level && sensorValue_fr<level && sensorValue_bl<level && sensorValue_br>level){}  0110            
		else if(sensorValue_fl>level && sensorValue_fr<level && sensorValue_bl>level && sensorValue_br<level)//0101                
				{range_f(); //执行测距函数                 
				if(S_r>30 && S_m>30)                    
					{R();}}            
		else if(sensorValue_fl>level && sensorValue_fr>level && sensorValue_bl<level && sensorValue_br<level)//0011                
				{range_b(); //执行测距函数                 
				if(S_b>30)                    
					back();                  
				}            
		else if(sensorValue_fl>level && sensorValue_fr<level && sensorValue_bl<level && sensorValue_br<level)//0111                
				{L();}            
		else if(sensorValue_fl<level && sensorValue_fr>level && sensorValue_bl<level && sensorValue_br<level)//1011                
				{R();}            
		else if(sensorValue_fl<level && sensorValue_fr<level && sensorValue_bl>level && sensorValue_br<level)//1101                
				{R();}            
		else if(sensorValue_fl<level && sensorValue_fr<level && sensorValue_bl<level && sensorValue_br>level)//1110                
				{L();}            
				   
		else   
				{line();    
				delay(5000);    
				lull();}
		}}				
if(water_test>water_level && box>300)//如果土壤湿度值较低且水箱有水   
	{digitalWrite(water_machine,HIGH);}   //给水泵使能给植物浇水   
else   
	digitalWrite(water_machine,LOW);       
	 
}
 
 
//void turn(){ 
//判断转向函数 
//lull(); 
//停止所用电机 
//s.write(170); 
//舵机转到 170 度既左边（角度与安装方式有关） 
//delay(500); 
//留时间给舵机转向 
//range_f(); 
//运行测距函数 
//s.write(90); 
//测距完成，舵机回到中位 
//delay(600); 
//留时间给舵机转向 
//if (S>30) {L();} 
//判断左边障碍物距离，如果距离充足,运行左转  
//else { //s.write(10); 
//否则，舵机转动到 10 度，测右边距离 
//delay(600); //range_f(); 
//测距 
//s.write(90); 
//中位 
//delay(600); 
//if(S>30){ R(); //} 
//右转 //else{ back(); 
//判断右边距离，距离充足右转否则后退 
//int x=random(1); 
//产生一个 0 到 1 的随机数  
//if (x=0){R();}  

 
//else{L();} 
//判断随机数 
//} 
//否则后退，并随机转向 
//} 
//} 
 
 
void range_f(){ //测距函数 
s.write(90); //舵机中位 
delay(500); //留时间给舵机转向 
digitalWrite(trig_f,LOW); //测距 
delayMicroseconds(2); //延时 2 微秒 
digitalWrite(trig_f,HIGH); 
delayMicroseconds(20); 
digitalWrite(trig_f,LOW); 
int distance = pulseIn(echo_f,HIGH); //读取高电平时间 
distance = distance/58; //按照公式计算 
S_m = distance; //把值赋给 S 
 
s.write(45); //舵机 
delay(500); //留时间给舵机转向 
digitalWrite(trig_f,LOW); //测距 
delayMicroseconds(2); //延时 2 微秒 
digitalWrite(trig_f,HIGH); 
delayMicroseconds(20); 
digitalWrite(trig_f,LOW); 
distance = pulseIn(echo_f,HIGH); //读取高电平时间 
distance = distance/58; //按照公式计算 
S_l = distance; //把值赋给 S 
 
s.write(135); //舵机 
delay(500); //留时间给舵机转向 
digitalWrite(trig_f,LOW); //测距 
delayMicroseconds(2); //延时 2 微秒 
digitalWrite(trig_f,HIGH); 
delayMicroseconds(20); 
digitalWrite(trig_f,LOW); 
distance = pulseIn(echo_f,HIGH); //读取高电平时间 
distance = distance/58; //按照公式计算 
S_r = distance; //把值赋给 S 
//Serial.println(S); //向串口发送 S 的值，可以在显示器上显示距离 
//if (S<30){ 
//tone(12,800,50); 
//delay(50); 
//延时 
//} 

} 
 
void range_b(){ //测距函数 
digitalWrite(trig_b,LOW); //测距 
delayMicroseconds(2); //延时 2 微秒 
digitalWrite(trig_b,HIGH); 
delayMicroseconds(20); 
digitalWrite(trig_b,LOW); 
int distanceb = pulseIn(echo_b,HIGH); //读取高电平时间 
distanceb = distanceb/58; //按照公式计算 
S_b = distanceb; //把值赋给 S 
//Serial.println(S); //向串口发送 S 的值，可以在显示器上显示距离 
//if (S<30){ 
//tone(12,800,50); 
//delay(50); 
//延时} 
} 
 
 
 
void line(){//前进 
digitalWrite(motorR1,HIGH); //启动所有电机向前 
digitalWrite(motorL1,HIGH); 
digitalWrite(motorR2,LOW); 
digitalWrite(motorL2,LOW); 
} 
 
void L(){//左转 
digitalWrite(motorL1,LOW); 
digitalWrite(motorR2,LOW); 
analogWrite(motorL2,100); 
analogWrite(motorR1,100); 
//delay(500); 
//lull(); 
//暂停所有电机 
} 
 
 
void R(){//右转 
digitalWrite(motorL2,LOW); 
digitalWrite(motorR1,LOW); 
analogWrite(motorL1,100); 
analogWrite(motorR2,100); 
//delay(500); 
//lull(); } 
 
 
 
void back(){ //后退函数 
digitalWrite(motorL1,LOW); 
digitalWrite(motorR1,LOW); 
analogWrite(motorL2,100); 
analogWrite(motorR2,100); 
//delay(500); 
} 
 
void lull(){//停止 
digitalWrite(motorL1,LOW); 
digitalWrite(motorL2,LOW); 
digitalWrite(motorR1,LOW); 
digitalWrite(motorR2,LOW); 
} 
 