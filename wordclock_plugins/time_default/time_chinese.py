
class time_chinese:
    """
    This class returns a given time as a range of LED-indices.
    Illuminating these LEDs represents the current time on a chinese WCA 10x10 (last 2 lines are fully dummy)

	It shows the time both in Chinese characters as in how to pronounce them,
	and additionally has a bonus sentence and some bonus words in Chinese characters:
	* Beautiful           - 佳         pronounced as Jiā
	* Love                - 爱         pronounced as Ài
	* Heart               - 心         pronounced as Xīn
	* Practice/experience - 练         pronounced as Liàn
    * Happy               - 高兴	       pronounced as Gāoxìng	
    	
	I have used this explanation https://improvemandarin.com/tell-time-in-chinese/
	In general: It is <hours> o'clock <minutes> / 1 or 3 quarters past / half past
	So no term for Minutes (not needed in non-formal chinese) and no X minutes before...
	On last thing: when using 5 minutes past, an extra "Ling" must be used for "zero-five".
		

   range(0,2) + range(12,13) + range(21,28) + range(63,67): 
    	It is ... o'clock: 现在 ... 点 and XIÀNZÀI  ... DIǍN 

    十两		SHÍ ÈR		Twelve	range(2,3) + range()
    一		YĪ			One       range(51,54)
    两		ÈR			Two       range(55,59) 
    三		SÃN			Three     range(62,66) 
    四		SÌ			Four      range(66,70) 
    五		WǓ			Five      range(70,74) 
    六		LIÙ			Six       range(74,77) 
    七		QĪ			Seven     range(77,82) 
    八		BÃ			Eight     range(88,92) 
    九		JIÛ			Nine      range(83,88) 
    十		SHÍ			Ten       range(91,95) 
    十一		SHÍ YĪ		Eleven    range(96,99) 
    十两		SHÍ ÈR		Twelve    range(99,105) 

    零五		LÍNG WǓ		Five past           
    十		SHÍ			Ten past            
    一刻		YĪ KÈ		One quarter past    
    两十		ÈR SHÍ		Twenty past         
    两十五	ÈR SHÍ WǓ	Twenty five past    
    半		BÀN			Half past           
    三十五	SÃN SHÍ WǓ	Thirty five past    
    四		SÌ SHÍ		Fourty past         
    三刻		SÃN KÈ		Three quarters past 
    五十		WǓ SHÍ		Fifty past          
    五十五	WǓ SHÍ WǓ	Fifty five past     


    self.full_hour= n/a
    """

    def __init__(self):
        self.prefix = list(range(0,2)) +  list(range(12,13)) + list(range(25,29)) + list(range(30,33)) + list(range(60,64))
        self.hours= [\
            list(range(2,3)) + list(range(4,5)) + list(range(34,37)) + list(range(42,44)), \
            list(range(3,4))                    + list(range(40,42)), \
            list(range(4,5))                    + list(range(42,44)), \
            list(range(5,6))                    + list(range(37,40)), \
            list(range(6,7))                    + list(range(52,54)), \
            list(range(7,8))                    + list(range(50,52)), \
            list(range(8,9))                    + list(range(44,48)), \
            list(range(9,10))                   + list(range(54,56)), \
            list(range(10,11))                  + list(range(56,58)), \
            list(range(11,12))                  + list(range(47,50)), \
            list(range(2,3))                    + list(range(34,37)), \
            list(range(2,3)) + list(range(3,4)) + list(range(34,37)) + list(range(40,42)), \
            list(range(2,3)) + list(range(4,5)) + list(range(34,37)) + list(range(42,44))]
        self.minutes=[[], \
            list(range(22,23)) + list(range(23,24))                      + list(range(83,87)) + list(range(88,90)), \
            list(range(21,22))                                           + list(range(80,83)), \
            list(range(13,14)) + list(range(15,16))                      + list(range(68,70)) + list(range(75,77)), \
            list(range(17,18)) + list(range(21,22))                      + list(range(76,78)) + list(range(80,83)), \
            list(range(17,18)) + list(range(21,22)) + list(range(23,24)) + list(range(76,78)) + list(range(80,83)) + list(range(88,90)), \
            list(range(16,17)) + list(range(72,75)), \
            list(range(14,15)) + list(range(21,22)) + list(range(23,24)) + list(range(65,68)) + list(range(80,83)) + list(range(88,90)), \
            list(range(19,20)) + list(range(21,22))                      + list(range(78,80)) + list(range(80,83)), \
            list(range(14,15)) + list(range(15,16))                      + list(range(65,68)) + list(range(75,77)), \
            list(range(70,72)) + list(range(21,22))                      + list(range(70,72)) + list(range(80,83)), \
            list(range(70,72)) + list(range(21,22)) + list(range(23,24)) + list(range(70,72)) + list(range(80,83)) + list(range(88,90))]
        self.full_hour= []

    def get_time(self, time, purist):
        hour=time.hour%12 #+(1 if time.minute//5 > 3 else 0)
        minute=time.minute//5
        # Assemble indices
        return  \
            (self.prefix if not purist else []) + \
            self.minutes[int(minute)] + \
            self.hours[hour] + \
            self.full_hour

