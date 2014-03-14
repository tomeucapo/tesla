//
//  Displays.h
//  iAnalitzador
//
//  Created by Tomeu Capó on 18/09/12.
//
//

#import <UIKit/UIKit.h>

@interface Displays : UIView {
    @private
    int coordY;
}

- (void)paint: (NSArray*)lValors withTitle:(NSString*)titleText;

@property (nonatomic, readonly) int coordY;

@end
