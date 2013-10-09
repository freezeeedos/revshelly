#!/usr/bin/perl
#The MIT License (MIT)
#
#Copyright (c) 2013 Quentin Gibert
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#the Software, and to permit persons to whom the Software is furnished to do so,
#subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
use strict;
use warnings;
no warnings "uninitialized";

use MIME::Base64;

open(my $f, "<", "$ARGV[0]");

our @f = <$f>;
my @files;
sub extract;

foreach(@f){
    if($_=~/BEGIN: (.*)$/){
        push @files, $1;
    }
}

foreach(@files){
    my $fname = $_;
    print qq{file: $fname\n};
    extract($fname);
    decode($fname);
}

sub extract{
    my $file = $_[0];
    my $i = 0;
    my $begin;
    my $end;

    print qq{extracting $file\n};

    open(DEST, ">", qq{$file.txt})
    or die qq{Could not open $file.txt: $!};

    foreach(@f){
        if($_=~/BEGIN: $file/){
            $begin = $i;
        }
        if($_=~/END: $file/){
            $end = $i;
        }
        $i++;
    }

    for($i=$begin+1;$i<$end;$i++){
        print DEST qq{$f[$i]};
    }
    close(DEST);
}

sub decode{
    my($fname) = @_;

    open(SRC, "<", qq{$fname.txt})
    or die qq{Could not open $fname.txt: $!};

    open(DEST, ">", qq{$fname})
    or die qq{Could not open $fname for reading: $!};

    while(<SRC>){
        my $line = $_;
        my $decoded = MIME::Base64::decode($line);
        print DEST $decoded;
    }

    close(SRC);
    close(DEST);
}
