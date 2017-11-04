# Packet Generator

Utility used for generating packet structure.

## Purpose

When you starting to develop your own protocol, one of the most important part of developing is building your packet structure. The Packet Generator allows you
to define your packet members and bit chunk size of those members. You can deploy your packet structure into your programming language and use that structure for
reading packets you have recieved or writing your packet insides to buffer. You also having ability to set values of members and store them to your buffer.

## Getting Started

In order to define your packet structure, you have to create structure file *.pg.
Which will basicly gonna look like:
```
MyPacketName
{
  MyFirstMember:10
  MySecondMember:30
  MyThirdMember:50
}
```
So packet generator will make you a structure, which will be named as "MyPacketName" and will have members:

MyFirstMember which will be at the beginning of your packet and will have 10 bits.
MySecondMember which will be second member of your packet and will have 30 bits.
MyThirdMember which will be at the end of your packet and will have 50 bits.

Now, when you defined your packet structure, you can run generator.py

At your command line like so:
```
python3 generator.py -language YourLanguage -input input.pg -output output
```
And now you ready to use your packet structure in your project.

The interface of packet structure consists of 4 public methods:

get(PacketMember, buffer) -> will copy member to buffer.
set(PacketMember, buffer) -> will copy member from buffer to packet.
read(buffer) -> will copy buffer to packet.
write(buffer) -> will copy packet to buffer.

## Requirements

PacketGenerator should be runned with python3.

## Authors

**Illia Shkroba**

## License

This project is an open source. So you can use it for your own purpose for free.

## Languages which are supported
  Java
  
  You can leave me a request, so I can add more if you want.
