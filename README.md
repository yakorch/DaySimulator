# DaySimulator
A day simulator using finite state machine implementation, where each state is an action during the day


Every day is different, so is every simulation. 

There are 7 main states, in which every student can be in:
    - sleep
    - eat
    - workout
    - study
    - shower
    - watch youtube
    - walking in the park


One state at one time - a rule for finite state machines!

There are certain rules for some states, like always eating after sleeping:

![Знімок екрана 2022-05-31 о 11 53 25](https://user-images.githubusercontent.com/92575094/171133951-c3ac3104-90db-4b6d-a9a8-9936c4f3d682.png)

And random ones, for example a character can choose to do anything after the shower:

![Знімок екрана 2022-05-31 о 11 53 43](https://user-images.githubusercontent.com/92575094/171134019-b8207593-dafd-45ad-8d3e-2f6f004ae54b.png)




Cycle method ends when 24 hours pass, as in reality. After the transition between states necessary info is printed

This is an example of the end of the simulation:

![Знімок екрана 2022-05-31 о 11 55 57](https://user-images.githubusercontent.com/92575094/171134533-7426b692-6ee7-4bf8-98c1-879488b59bae.png)

In the end simulation prints possible mental / physical state of a person! :)
