//
//  ConfigFieldViewController.h
//  iAnalitzador
//
//  Created by Tomeu Capó on 10/10/13.
//
//

#import <UIKit/UIKit.h>

@interface ConfigFieldViewController : UIViewController
{
    IBOutlet UILabel *fieldTitle;
    IBOutlet UITextField *fieldValue;
}

@property (nonatomic) UILabel* fieldTitle;

- (void) setField: (NSString*)title setValue: (NSString*)value;

@end
