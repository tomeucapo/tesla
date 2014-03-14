//
//  Displays.m
//  Classe per representar un valor o valors d'una variable obtinguda del 
//  analitzador
//
//  Created by Tomeu Capó on 18/09/12.
//

#import "Displays.h"

@implementation Displays
@synthesize coordY;

- (id)init
{
    self = [super init];
    if (self) {
        coordY = 0;
        self.backgroundColor = [UIColor lightGrayColor];
    }
    return self;
}

- (id)initWithFrame:(CGRect)frame
{
    self = [super initWithFrame:frame];
    if (self) {
        coordY = 0;
        self.backgroundColor = [UIColor lightGrayColor];
    }
    return self;
}

- (UILabel*)createDisplayValue: (NSString *) val
{
    UILabel *myDisplay;

    myDisplay = [[UILabel alloc] initWithFrame:CGRectMake(0, 0, self.frame.size.width-30, 40)];
    myDisplay.font = [UIFont fontWithName:@"DBLCDTempBlack" size: 34.0];
    myDisplay.center = CGPointMake(self.frame.size.width/2, coordY);
    myDisplay.text = val;
    
    myDisplay.backgroundColor = [UIColor darkGrayColor];
    myDisplay.textColor = [UIColor lightGrayColor];
    myDisplay.textAlignment = NSTextAlignmentRight;
    
    coordY+=40;
    return myDisplay;
}

- (void)paint: (NSArray*)lValors withTitle:(NSString*)titleText
{
    self.frame = CGRectMake(0, 0, self.frame.size.width, self.frame.size.height+30+(40*[lValors count]));
    
    NSNumberFormatter *formatter = [[NSNumberFormatter alloc] init];
    [formatter setNumberStyle:NSNumberFormatterDecimalStyle];

    UILabel *title = [[UILabel alloc] initWithFrame:CGRectMake(0,0,self.frame.size.width-30,20)];
    title.font = [UIFont fontWithName:@"System" size: 12];
    title.text = titleText;
    title.textColor = [UIColor darkGrayColor];
    title.center = CGPointMake(self.frame.size.width/2, 0);
    title.textAlignment = NSTextAlignmentLeft;
    
    coordY=30;
    [self addSubview: title];

    for(id v in lValors)
    {
        NSDecimalNumber *val = v;
        [self addSubview: [self createDisplayValue: [NSString stringWithFormat:@"%@", [formatter stringFromNumber: val] ]]];
    }
  
}


// Only override drawRect: if you perform custom drawing.
// An empty implementation adversely affects performance during animation.
- (void)drawRect:(CGRect)rect
{

}


@end
