#!/usr/bin/env python

import os
import configparser
import Command
from generators.Generator import Generator
import batoceraFiles
import shutil

vpinballConfigPath = batoceraFiles.CONF + "/vpinball"
vpinballConfigFileSource = vpinballConfigPath + "/VPinballX.ini"
vpinballConfigFile = vpinballConfigPath + "/VPinballX-configgen.ini"

class VPinballGenerator(Generator):

    def generate(self, system, rom, playersControllers, guns, wheels, gameResolution):

        # create vpinball config directory and default config file if they don't exist
        if not os.path.exists(vpinballConfigPath):
            os.makedirs(vpinballConfigPath)
        if not os.path.exists(vpinballConfigFileSource):
            shutil.copy("/usr/bin/vpinball/assets/Default VPinballX.ini", vpinballConfigFileSource)
        # all the modifications will be applied to the VPinballX-configgen.ini which is a copy of the VPinballX.ini
        shutil.copy(vpinballConfigFileSource, vpinballConfigFile)            

        #VideogetCurrentResolution to convert from percentage to pixel value
        #necessary because people can plug their 1080p laptop on a 4k TV
        def ConvertToPixel(total_size,percentage):
            pixel_value = str(int(int(total_size)*float(percentage)*1e-2))
            return pixel_value
        # Calculates the relative height, depending on the screen ratio
        # (normaly 16/9), the element ratio (4/3 for the b2s) and the relative width
        def RelativeHeightCalculate(Rscreen,Relement,RelativeWidth):
            return int(Rscreen*RelativeWidth/Relement)

        ## [ VPinballX-configgen.ini ] ##
        vpinballSettings = configparser.ConfigParser(interpolation=None)
        # To prevent ConfigParser from converting to lower case
        vpinballSettings.optionxform = str
        vpinballSettings.read(vpinballConfigFile)
        # Sections
        if not vpinballSettings.has_section("Standalone"):
            vpinballSettings.add_section("Standalone")
        if not vpinballSettings.has_section("Player"):
            vpinballSettings.add_section("Player")

        # Expert Users have the possibility to not use the configgen at all (switchon)
        if system.isOptSet("vpinball_disableconfiggen"):
            pass
        else:
            #Tables are organised by folders containing the vpx file, and sub-folders with the roms, altcolor, altsound,...We keep a switch to allow users with the old unique pinmame to be able to continue using vpinball (switchon)
            if system.isOptSet("vpinball_folders"):
                vpinballSettings.set("Standalone", "PinMAMEPath", "")
            else:
                vpinballSettings.set("Standalone", "PinMAMEPath", "./")
            #Ball trail
            if system.isOptSet("vpinball_balltrail"):
                vpinballSettings.set("Player", "BallTrail", "1")
                vpinballSettings.set("Player", "BallTrailStrength", system.config["vpinball_balltrail"])
            else:
                vpinballSettings.set("Player", "BallTrail", "0")
                vpinballSettings.set("Player", "BallTrailStrength", "0")
            #Visual Nugde Strength
            if system.isOptSet("vpinball_nudgestrength"):
                vpinballSettings.set("Player", "NudgeStrength", system.config["vpinball_nudgestrength"])
            else:
                vpinballSettings.set("Player", "NudgeStrength", "")
            # Performance settings
            if system.isOptSet("vpinball_maxframerate"):
                vpinballSettings.set("Player", "MaxFramerate", system.config["vpinball_maxframerate"])
            else:
                vpinballSettings.set("Player", "MaxFramerate", "")
            if system.isOptSet("vpinball_vsync"):
                vpinballSettings.set("Player", "SyncMode", system.config["vpinball_vsync"])
            else:
                vpinballSettings.set("Player", "SyncMode", "2")
            if system.isOptSet("vpinball_presets"):
                if system.config["vpinball_presets"]=="defaults":
                    vpinballSettings.set("Player", "FXAA", "")
                    vpinballSettings.set("Player", "Sharpen", "")
                    vpinballSettings.set("Player", "DisableAO", "")
                    vpinballSettings.set("Player", "DynamicAO", "")
                    vpinballSettings.set("Player", "SSRefl", "")
                    vpinballSettings.set("Player", "PFReflection", "")
                    vpinballSettings.set("Player", "ForceAnisotropicFiltering", "")
                    vpinballSettings.set("Player", "AlphaRampAccuracy", "")     
                if system.config["vpinball_presets"]=="highend":
                    vpinballSettings.set("Player", "FXAA", "3")
                    vpinballSettings.set("Player", "Sharpen", "2")
                    vpinballSettings.set("Player", "DisableAO", "0")
                    vpinballSettings.set("Player", "DynamicAO", "1")
                    vpinballSettings.set("Player", "SSRefl", "1")
                    vpinballSettings.set("Player", "PFReflection", "5")
                    vpinballSettings.set("Player", "ForceAnisotropicFiltering", "1")
                    vpinballSettings.set("Player", "AlphaRampAccuracy", "10")
                if system.config["vpinball_presets"]=="lowend":
                    vpinballSettings.set("Player", "FXAA", "0")
                    vpinballSettings.set("Player", "Sharpen", "0")
                    vpinballSettings.set("Player", "DisableAO", "1")
                    vpinballSettings.set("Player", "DynamicAO", "0")
                    vpinballSettings.set("Player", "SSRefl", "0")
                    vpinballSettings.set("Player", "PFReflection", "3")
                    vpinballSettings.set("Player", "ForceAnisotropicFiltering", "0")
                    vpinballSettings.set("Player", "AlphaRampAccuracy", "5")
                # if nothing is specified, we're in manual settings, ie we don't change any value in the config file

            #Altcolor (switchon)
            if system.isOptSet("vpinball_altcolor"):
                vpinballSettings.set("Standalone", "AltColor", "0")
            else:
                vpinballSettings.set("Standalone", "AltColor","1")

            Rscreen=16/9            
            # PinMAME DMD
            Rpinmame=4/1
            if system.isOptSet("vpinball_pinmame"):
                pinmamex,pinmamey,pinmamewidth=75,0,25   #default values
                #pinmameheight=RelativeHeightCalculate(Rscreen,Rpinmame,pinmamewidth)
                # pinmamedmdx,pinmamedmdy,pinmamedmdwidth,pinmamedmdheight=75,33,25,14
                if system.config["vpinball_pinmame"]=="pinmame_disabled":
                    # vpinballSettings.set("Standalone", "B2SHideGrill","")
                    vpinballSettings.set("Standalone", "PinMAMEWindow","0")
                    # vpinballSettings.set("Standalone", "B2SHideB2SDMD","1")
                else:
                    # vpinballSettings.set("Standalone", "B2SHideGrill","1")
                    vpinballSettings.set("Standalone", "PinMAMEWindow","1")
                    # vpinballSettings.set("Standalone", "B2SHideB2SDMD","0")
                if system.config["vpinball_pinmame"]=="pinmame_topright_small":
                    pinmamex,pinmamey,pinmamewidth=80,0,20   #default values
                    #pinmameheight=RelativeHeightCalculate(Rscreen,Rpinmame,pinmamewidth)
                    # pinmamedmdx,pinmamedmdy,pinmamedmdwidth,pinmamedmdheight=80,27,20,11
                if system.config["vpinball_pinmame"]=="pinmame_topright_medium":
                    pinmamex,pinmamey,pinmamewidth=75,0,25   #default values
                    #pinmameheight=RelativeHeightCalculate(Rscreen,Rpinmame,pinmamewidth)
                    # pinmamedmdx,pinmamedmdy,pinmamedmdwidth,pinmamedmdheight=75,33,25,14
                if system.config["vpinball_pinmame"]=="pinmame_topright_large":
                    pinmamex,pinmamey,pinmamewidth=70,0,30   #default values
                    #pinmameheight=RelativeHeightCalculate(Rscreen,Rpinmame,pinmamewidth)
                    # pinmamedmdx,pinmamedmdy,pinmamedmdwidth,pinmamedmdheight=70,40,30,17
                if system.config["vpinball_pinmame"]=="pinmame_topleft_small":
                    pinmamex,pinmamey,pinmamewidth=0,0,20   #default values
                    #pinmameheight=RelativeHeightCalculate(Rscreen,Rpinmame,pinmamewidth)
                    # pinmamedmdx,pinmamedmdy,pinmamedmdwidth,pinmamedmdheight=0,27,20,11
                if system.config["vpinball_pinmame"]=="pinmame_topleft_medium":
                    pinmamex,pinmamey,pinmamewidth=0,0,25   #default values
                    #pinmameheight=RelativeHeightCalculate(Rscreen,Rpinmame,pinmamewidth)
                    # pinmamedmdx,pinmamedmdy,pinmamedmdwidth,pinmamedmdheight=0,33,25,14
                if system.config["vpinball_pinmame"]=="pinmame_topleft_large":
                    pinmamex,pinmamey,pinmamewidth=0,0,30   #default values
                   #pinmameheight=RelativeHeightCalculate(Rscreen,Rpinmame,pinmamewidth)
                    # pinmamedmdx,pinmamedmdy,pinmamedmdwidth,pinmamedmdheight=0,40,30,17
                # apply settings
                pinmameheight=RelativeHeightCalculate(Rscreen,Rpinmame,pinmamewidth)
                vpinballSettings.set("Standalone", "PinMAMEWindowX",ConvertToPixel(gameResolution["width"],pinmamex))
                vpinballSettings.set("Standalone", "PinMAMEWindowY",ConvertToPixel(gameResolution["height"],pinmamey))
                vpinballSettings.set("Standalone", "PinMAMEWindowWidth",ConvertToPixel(gameResolution["width"],pinmamewidth))
                vpinballSettings.set("Standalone", "PinMAMEWindowHeight",ConvertToPixel(gameResolution["height"],pinmameheight))
            #
            # #PinMAMEWindow (switch)
            # if system.isOptSet("vpinball_pinmamewindow"):
            #     vpinballSettings.set("Standalone", "PinMAMEWindow","1")
            # else:
            #     vpinballSettings.set("Standalone", "PinMAMEWindow","0")
            # if system.isOptSet("vpinball_pinmamewindowx"):
            #     vpinballSettings.set("Standalone", "PinMAMEWindowX",ConvertToPixel(gameResolution["width"],system.config["vpinball_pinmamewindowx"]))
            # else:
            #     vpinballSettings.set("Standalone", "PinMAMEWindowX","")
            # if system.isOptSet("vpinball_pinmamewindowy"):
            #     vpinballSettings.set("Standalone", "PinMAMEWindowY",ConvertToPixel(gameResolution["height"],system.config["vpinball_pinmamewindowy"]))
            # else:
            #     vpinballSettings.set("Standalone", "PinMAMEWindowY","")
            # if system.isOptSet("vpinball_pinmamewindowwidth"):
            #     vpinballSettings.set("Standalone", "PinMAMEWindowWidth",ConvertToPixel(gameResolution["width"],system.config["vpinball_pinmamewindowwidth"]))
            # else:
            #     vpinballSettings.set("Standalone", "PinMAMEWindowWidth","")
            # if system.isOptSet("vpinball_pinmamewindowheight"):
            #     vpinballSettings.set("Standalone", "PinMAMEWindowHeight",ConvertToPixel(gameResolution["height"],system.config["vpinball_pinmamewindowheight"]))
            # else:
            #     vpinballSettings.set("Standalone", "PinMAMEWindowHeight","")

            # FLEXDMD
            if system.isOptSet("vpinball_flexdmd"):
                flexdmdx,flexdmdy,flexdmdwidth,flexdmdheight=75,0,25,14   #default values
                flexdmdheight
                # flexdmddmdx,flexdmddmdy,flexdmddmdwidth,flexdmddmdheight=75,33,25,14
                if system.config["vpinball_flexdmd"]=="flexdmd_disabled":                                            
                    # vpinballSettings.set("Standalone", "B2SHideGrill","")        
                    vpinballSettings.set("Standalone", "FlexDMDWindow","0")
                    # vpinballSettings.set("Standalone", "B2SHideB2SDMD","1")        
                else:
                    # vpinballSettings.set("Standalone", "B2SHideGrill","1")        
                    vpinballSettings.set("Standalone", "FlexDMDWindow","1")
                    # vpinballSettings.set("Standalone", "B2SHideB2SDMD","0")
                if system.config["vpinball_flexdmd"]=="flexdmd_topright_small":                                            
                    flexdmdx,flexdmdy,flexdmdwidth,flexdmdheight=80,0,20,9   #default values
                    # flexdmddmdx,flexdmddmdy,flexdmddmdwidth,flexdmddmdheight=80,27,20,11
                if system.config["vpinball_flexdmd"]=="flexdmd_topright_medium":                                            
                    flexdmdx,flexdmdy,flexdmdwidth,flexdmdheight=75,0,25,11   #default values
                    # flexdmddmdx,flexdmddmdy,flexdmddmdwidth,flexdmddmdheight=75,33,25,14
                if system.config["vpinball_flexdmd"]=="flexdmd_topright_large":                                            
                    flexdmdx,flexdmdy,flexdmdwidth,flexdmdheight=70,0,30,13   #default values
                    # flexdmddmdx,flexdmddmdy,flexdmddmdwidth,flexdmddmdheight=70,40,30,17
                if system.config["vpinball_flexdmd"]=="flexdmd_topleft_small":                                            
                    flexdmdx,flexdmdy,flexdmdwidth,flexdmdheight=0,0,20,9   #default values
                    # flexdmddmdx,flexdmddmdy,flexdmddmdwidth,flexdmddmdheight=0,27,20,11
                if system.config["vpinball_flexdmd"]=="flexdmd_topleft_medium":                                            
                    flexdmdx,flexdmdy,flexdmdwidth,flexdmdheight=0,0,25,11   #default values
                    # flexdmddmdx,flexdmddmdy,flexdmddmdwidth,flexdmddmdheight=0,33,25,14
                if system.config["vpinball_flexdmd"]=="flexdmd_topleft_large":                                            
                    flexdmdx,flexdmdy,flexdmdwidth,flexdmdheight=0,0,30,13   #default values
                    # flexdmddmdx,flexdmddmdy,flexdmddmdwidth,flexdmddmdheight=0,40,30,17                   
                # apply settings
                vpinballSettings.set("Standalone", "FlexDMDWindowX",ConvertToPixel(gameResolution["width"],flexdmdx))
                vpinballSettings.set("Standalone", "FlexDMDWindowY",ConvertToPixel(gameResolution["height"],flexdmdy))
                vpinballSettings.set("Standalone", "FlexDMDWindowWidth",ConvertToPixel(gameResolution["width"],flexdmdwidth))
                vpinballSettings.set("Standalone", "FlexDMDWindowHeight",ConvertToPixel(gameResolution["height"],flexdmdheight))
                
            # B2S Easy Mode.
            if system.isOptSet("vpinball_b2s"):
                b2sx,b2sy,b2swidth,b2sheight=75,0,25,33   #default values
                b2sdmdx,b2sdmdy,b2sdmdwidth,b2sdmdheight=75,33,25,14
                if system.config["vpinball_b2s"]=="b2s_disabled":                                            
                    vpinballSettings.set("Standalone", "B2SHideGrill","")        
                    vpinballSettings.set("Standalone", "B2SWindows","0")
                    vpinballSettings.set("Standalone", "B2SHideB2SDMD","1")        
                else:
                    vpinballSettings.set("Standalone", "B2SHideGrill","1")        
                    vpinballSettings.set("Standalone", "B2SWindows","1")
                    vpinballSettings.set("Standalone", "B2SHideB2SDMD","0")
                if system.config["vpinball_b2s"]=="b2s_topright_small":                                            
                    b2sx,b2sy,b2swidth,b2sheight=80,0,20,27   #default values
                    b2sdmdx,b2sdmdy,b2sdmdwidth,b2sdmdheight=80,27,20,11
                if system.config["vpinball_b2s"]=="b2s_topright_medium":                                            
                    b2sx,b2sy,b2swidth,b2sheight=75,0,25,33   #default values
                    b2sdmdx,b2sdmdy,b2sdmdwidth,b2sdmdheight=75,33,25,14
                if system.config["vpinball_b2s"]=="b2s_topright_large":                                            
                    b2sx,b2sy,b2swidth,b2sheight=70,0,30,40   #default values
                    b2sdmdx,b2sdmdy,b2sdmdwidth,b2sdmdheight=70,40,30,17
                if system.config["vpinball_b2s"]=="b2s_topleft_small":                                            
                    b2sx,b2sy,b2swidth,b2sheight=0,0,20,27   #default values
                    b2sdmdx,b2sdmdy,b2sdmdwidth,b2sdmdheight=0,27,20,11
                if system.config["vpinball_b2s"]=="b2s_topleft_medium":                                            
                    b2sx,b2sy,b2swidth,b2sheight=0,0,25,33   #default values
                    b2sdmdx,b2sdmdy,b2sdmdwidth,b2sdmdheight=0,33,25,14
                if system.config["vpinball_b2s"]=="b2s_topleft_large":                                            
                    b2sx,b2sy,b2swidth,b2sheight=0,0,30,40   #default values
                    b2sdmdx,b2sdmdy,b2sdmdwidth,b2sdmdheight=0,40,30,17                   
                # apply settings
                vpinballSettings.set("Standalone", "B2SBackglassX",ConvertToPixel(gameResolution["width"],b2sx))
                vpinballSettings.set("Standalone", "B2SBackglassY",ConvertToPixel(gameResolution["height"],b2sy))                
                vpinballSettings.set("Standalone", "B2SBackglassWidth",ConvertToPixel(gameResolution["width"],b2swidth))
                vpinballSettings.set("Standalone", "B2SBackglassHeight",ConvertToPixel(gameResolution["height"],b2sheight))
                vpinballSettings.set("Standalone", "B2SDMDX",ConvertToPixel(gameResolution["width"],b2sdmdx))
                vpinballSettings.set("Standalone", "B2SDMDY",ConvertToPixel(gameResolution["height"],b2sdmdy))
                vpinballSettings.set("Standalone", "B2SDMDWidth",ConvertToPixel(gameResolution["width"],b2sdmdwidth))
                vpinballSettings.set("Standalone", "B2SDMDHeight",ConvertToPixel(gameResolution["height"],b2sdmdheight))
                    

#             if system.isOptSet("vpinball_b2seasymode"):
#                 if system.config["vpinball_presets"]=="topleftdmd":                
#                     b2sx,b2sy,b2switdth,b2sheight=0,0,25,33   #default values
#                     b2sdmdx,b2sdmdy,b2sdmdwidth,b2sdmdheight=0,33,25,14
#                     # vpinballSettings.set("Standalone", "B2SHideB2SDMD","0")
#                 if system.config["vpinball_presets"]=="topleftnodmd":                
#                     b2sx,b2sy,b2switdth,b2sheight=0,0,25,33   #default values
#                     # b2sdmdx,b2sdmdy,b2sdmdwidth,b2sdmdheight=0,33,25,14
#                     vpinballSettings.set("Standalone", "B2SHideB2SDMD","1")
#                 if system.config["vpinball_presets"]=="toprightnodmd":                
#                     b2sx,b2sy,b2switdth,b2sheight=0,0,25,33   #default values
#                     # b2sdmdx,b2sdmdy,b2sdmdwidth,b2sdmdheight=0,33,25,14
#                     vpinballSettings.set("Standalone", "B2SHideB2SDMD","1")
#                     
#             
#             #B2SWindows (switchon)
#             if system.isOptSet("vpinball_b2swindows"):
#                 vpinballSettings.set("Standalone", "B2SWindows","0")
#             else:
#                 vpinballSettings.set("Standalone", "B2SWindows","1")
#             if system.isOptSet("vpinball_b2sbackglassx"):
#                 vpinballSettings.set("Standalone", "B2SBackglassX",ConvertToPixel(gameResolution["width"],system.config["vpinball_b2sbackglassx"]))
#             else:
#                 vpinballSettings.set("Standalone", "B2SBackglassX","")
#             if system.isOptSet("vpinball_b2sbackglassy"):
#                 vpinballSettings.set("Standalone", "B2SBackglassY",ConvertToPixel(gameResolution["height"],system.config["vpinball_b2sbackglassy"]))
#             else:
#                 vpinballSettings.set("Standalone", "B2SBackglassY","")           
#             if system.isOptSet("vpinball_b2sbackglasswidth"):
#                 vpinballSettings.set("Standalone", "B2SBackglassWidth",ConvertToPixel(gameResolution["width"],system.config["vpinball_b2sbackglasswidth"]))
#             else:
#                 vpinballSettings.set("Standalone", "B2SBackglassWidth","")
#             if system.isOptSet("vpinball_b2sbackglassheight"):
#                 vpinballSettings.set("Standalone", "B2SBackglassHeight",ConvertToPixel(gameResolution["height"],system.config["vpinball_b2sbackglassheight"]))
#             else:
#                 vpinballSettings.set("Standalone", "B2SBackglassHeight","")           
# 
#             #B2S Hide B2SDMD (switchon)
#             if system.isOptSet("vpinball_b2swindows"):
#                 vpinballSettings.set("Standalone", "B2SHideB2SDMD","0")
#             else:
#                 vpinballSettings.set("Standalone", "B2SHideB2SDMD","1")
#             if system.isOptSet("vpinball_b2sdmdx"):
#                 vpinballSettings.set("Standalone", "B2SDMDX",ConvertToPixel(gameResolution["width"],system.config["vpinball_b2sdmdx"]))
#             else:
#                 vpinballSettings.set("Standalone", "B2SDMDX","")
#             if system.isOptSet("vpinball_b2sdmdy"):
#                 vpinballSettings.set("Standalone", "B2SDMDY",ConvertToPixel(gameResolution["height"],system.config["vpinball_b2sdmdy"]))
#             else:
#                 vpinballSettings.set("Standalone", "B2SDMDY","")           
#             if system.isOptSet("vpinball_b2sdmdwidth"):
#                 vpinballSettings.set("Standalone", "B2SDMDWidth",ConvertToPixel(gameResolution["width"],system.config["vpinball_b2sdmdwidth"]))
#             else:
#                 vpinballSettings.set("Standalone", "B2SDMDWidth","")
#             if system.isOptSet("vpinball_b2sdmdheight"):
#                 vpinballSettings.set("Standalone", "B2SDMDHeight",ConvertToPixel(gameResolution["height"],system.config["vpinball_b2sdmdheight"]))
#             else:
#                 vpinballSettings.set("Standalone", "B2SDMDHeight","")           
# 
#             #Sound balance
#             if system.isOptSet("vpinball_musicvolume"):
#                 vpinballSettings.set("Player", "MusicVolume", system.config["vpinball_musicvolume"])
#             else:
#                 vpinballSettings.set("Player", "MusicVolume", "")
#             if system.isOptSet("vpinball_soundvolume"):
#                 vpinballSettings.set("Player", "SoundVolume", system.config["vpinball_soundvolume"])
#             else:
#                 vpinballSettings.set("Player", "SoundVolume", "")
#             #Altsound
#             if system.isOptSet("vpinball_altsound"):
#                 vpinballSettings.set("Standalone", "AltSound", system.config["vpinball_altsound"])
#             else:
#                 vpinballSettings.set("Standalone", "AltSound","1")


        # Save VPinballX.ini
        with open(vpinballConfigFile, 'w') as configfile:
            vpinballSettings.write(configfile)

        # set the config path to be sure
        commandArray = [
            "/usr/bin/vpinball/VPinballX_GL",
            "-PrefPath", vpinballConfigPath,
            "-Ini", vpinballConfigFile,
            "-Play", rom
        ]
        return Command.Command(array=commandArray)

    def getInGameRatio(self, config, gameResolution, rom):
        return 16/9
