#!/usr/bin/env python3
"""
AudioTally - Multiple Events Duration Calculator

Beautiful modern desktop app to calculate total duration of copied Cubase/Nuendo clips.
Uses CustomTkinter for modern, rounded buttons and native dark mode support.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter
import xml.etree.ElementTree as ET
import subprocess
import json
import os
from PIL import Image, ImageDraw

# Set CustomTkinter appearance and theme
customtkinter.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"  
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (default), "green", "dark-blue"

# Configuration file to remember user preferences
CONFIG_FILE = os.path.expanduser("~/.cubase-nuendo_duration_calc_config.json")

class NuendoDurationCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("AudioTally - Multiple Events Duration Calculator for Cubase & Nuendo")
        self.root.geometry("600x500")  # Smaller initial size since details are hidden
        self.root.resizable(True, True)
        
        # Load saved configuration
        self.config = self.load_config()
        
        # Optimized clipboard tracking for better performance
        self.cached_clips = None
        self.cached_clipboard_content = ""
        self.original_clipboard_content = ""  # Store original XML for restoration
        
        self.setup_ui()
        self.auto_check_clipboard()
        
    def load_config(self):
        """Load user configuration"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {'last_sample_rate': '48000'}
    
    def save_config(self):
        """Save user configuration"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f)
        except:
            pass
    
    def setup_ui(self):
        """Create the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)  # Left column for buttons
        main_frame.columnconfigure(1, weight=1)  # Middle column
        main_frame.columnconfigure(2, weight=1)  # Right column for buttons
        main_frame.rowconfigure(9, weight=1)  # Updated for new layout - expandable area for results
        
        # Logo and Always-on-top setup
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "logo.png")
        
        # BIG TITLE "AudioTally" - Above logo, centered
        big_title_label = ttk.Label(main_frame, text="AudioTally", 
                               font=("Arial", 32, "bold"))
        big_title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # Logo (centered)
        logo_image = customtkinter.CTkImage(
            Image.open(logo_path),
            size=(128, 64)  # Width calculated from 512:256 ratio at 64px height
        )
        logo_label = customtkinter.CTkLabel(main_frame, image=logo_image, text="")
        logo_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))  # Centered across all 3 columns
        
        # Always-on-top toggle button (top-right corner)
        self.always_on_top = False  # Default state: not always on top
        self.setup_always_on_top_button(main_frame)
        
        # Description (smaller, not bold, under logo)
        description_label = ttk.Label(main_frame, text="Multiple Events Duration Calculator for Cubase & Nuendo", 
                               font=("Arial", 13))  # Smaller, not bold
        description_label.grid(row=2, column=0, columnspan=3, pady=(0, 20))
        
        # Instructions
        instructions = ttk.Label(main_frame, 
                                text="1. Select your project sample rate\n2. Select multiple clips in Cubase/Nuendo\n3. Copy them (Cmd+C)\n4. Results appear automatically!",
                                justify="left")
        instructions.grid(row=3, column=0, columnspan=3, pady=(0, 20), sticky=tk.W)
        
        # Sample rate selection
        ttk.Label(main_frame, text="Project Sample Rate:").grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.sample_rate_var = tk.StringVar()
        sample_rates = [
            ("8 kHz", "8000"),
            ("16 kHz", "16000"), 
            ("22.05 kHz", "22050"),
            ("32 kHz", "32000"),
            ("44.1 kHz", "44100"),
            ("48 kHz", "48000"),
            ("96 kHz", "96000"),
            ("192 kHz", "192000")
        ]
        
        self.sample_rate_combo = ttk.Combobox(main_frame, textvariable=self.sample_rate_var, 
                                             values=[f"{name}" for name, _ in sample_rates], 
                                             state="readonly", width=12)  # Optimized width to match content
        self.sample_rate_combo.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Set default value
        saved_rate = self.config.get('last_sample_rate', '48000')
        default_text = next((name for name, value in sample_rates if value == saved_rate), "48 kHz")
        self.sample_rate_combo.set(default_text)
        
        # Store the mapping for easy lookup
        self.rate_mapping = {name: value for name, value in sample_rates}
        
        # 3-Section Status Bar
        self.setup_status_bar(main_frame)
        
        # Calculate button - HIDDEN FOR AUTO-CALCULATION
        # self.calculate_btn = customtkinter.CTkButton(
        #     main_frame, 
        #     text="⏱️ Calculate Total Length",
        #     command=self.calculate_duration,
        #     height=40,  # Good height for touch targets
        #     font=customtkinter.CTkFont(size=14, weight="bold"),
        #     corner_radius=12,  # Rounded corners
        #     fg_color="#005BBB",      # darker blue idle color
        #     hover_color="#3399FF"    # lighter blue on hover
        # )
        # self.calculate_btn.grid(row=5, column=0, columnspan=3, pady=(0, 15), sticky='')  # Reduced padding
        
        # Remove ttk styling since we're using tk.Button now for better control
        
        # Configure main frame row for expandable area
        main_frame.rowconfigure(9, weight=1)
        
        # Big result display
        self.big_result_frame = ttk.Frame(main_frame, padding="10")  # Reduced padding
        self.big_result_frame.grid(row=7, column=0, columnspan=3, pady=(0, 15), sticky=(tk.W, tk.E))  # Reduced padding
        
        self.big_result_label = ttk.Label(self.big_result_frame, text="", 
                                         font=("Arial", 32, "bold"), foreground="#CDEFF7") # RESULT COLOR
        self.big_result_label.pack()
        
        # Show/Hide Details button - Initially hidden, will appear after calculation
        self.details_visible = tk.BooleanVar(value=False)
        
        # Use solid colors that mimic your gradient (no layering issues)
        self.toggle_details_btn = customtkinter.CTkButton(
            main_frame,
            text="📝 Show Details",
            command=self.toggle_details,
            height=40,  # Good height for touch targets  
            font=customtkinter.CTkFont(size=13, weight="bold"),
            corner_radius=12,  # Rounded corners
            fg_color="#1E1E3F",  # Middle color from your gradient
            hover_color="#2D2D5F",  # Bottom color from your gradient
            text_color="white"  # Ensure text is visible
        )
        # Don't grid it initially - it will be shown after calculation
        
        # Results area - Initially hidden
        self.results_frame = ttk.LabelFrame(main_frame, text="Detailed Results", padding="10")
        # Don't grid it initially - it will be shown/hidden by toggle
        
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(0, weight=1)
        
        # Results text widget with scrollbar - High contrast colors
        self.results_text = tk.Text(self.results_frame, height=20, wrap=tk.WORD, 
                                   font=("Monaco", 12), 
                                   bg="white", fg="black",  # High contrast: black text on white background
                                   relief=tk.SOLID, bd=1, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(self.results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Add placeholder text to show the area is working
        placeholder_text = "Detailed analysis will appear here...\n\n"
        placeholder_text += "📊 Individual clip durations\n"
        placeholder_text += "📈 Sample information\n" 
        placeholder_text += "🔊 Technical details\n"
        
        self.results_text.insert(1.0, placeholder_text)
        self.results_text.config(state=tk.DISABLED)  # Make read-only initially
        
        # Auto-detect is always enabled (simplified - no checkbox needed)
        self.auto_detect_var = tk.BooleanVar(value=True)
        
        self.last_result = ""
        
        # Initialize status to ready state
        self.set_status_ready()
    
    def setup_pin_tooltip(self):
        """Setup inline tooltip text for the pin button"""
        def on_enter(event):
            tooltip_text = "Unpin window" if self.always_on_top else "Pin window"
            self.pin_tooltip_label.configure(text=tooltip_text)
        
        def on_leave(event):
            self.pin_tooltip_label.configure(text="")
        
        # Bind mouse events to the pin button
        self.always_on_top_btn.bind('<Enter>', on_enter)
        self.always_on_top_btn.bind('<Leave>', on_leave)
    
    def setup_always_on_top_button(self, parent_frame):
        """Setup the always-on-top toggle button in the top-right corner"""
        assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        
        # Load pin icons
        unpinned_path = os.path.join(assets_path, "unpinned.png")
        pinned_path = os.path.join(assets_path, "pinned.png")
        
        # Create icon images (small size for top-right corner)
        self.unpinned_image = customtkinter.CTkImage(
            Image.open(unpinned_path),
            size=(20, 20)
        )
        self.pinned_image = customtkinter.CTkImage(
            Image.open(pinned_path),
            size=(20, 20)
        )
        
        # Create inline tooltip label (positioned to the left of the button)
        self.pin_tooltip_label = customtkinter.CTkLabel(
            parent_frame,
            text="",  # Initially empty
            font=customtkinter.CTkFont(size=10),
            text_color="white",
            fg_color="#333333",  # Dark background like a tooltip
            corner_radius=4,
            height=18,
            anchor="center",
            width=80  # Smaller width, closer to button
        )
        # Position closer to the pin button - right next to it
        self.pin_tooltip_label.place(relx=1.0, x=-45, y=8, anchor=tk.NE)
        
        # Always-on-top toggle button
        self.always_on_top_btn = customtkinter.CTkButton(
            parent_frame,
            image=self.unpinned_image,
            text="",  # No text, just icon
            width=28,  # Small square button
            height=28,
            command=self.toggle_always_on_top,
            fg_color="transparent",  # Transparent background
            hover_color="#404040",   # Subtle hover effect
            corner_radius=4
        )
        self.always_on_top_btn.grid(row=0, column=2, sticky=tk.NE, padx=(0, 5), pady=(5, 0))
        
        # Setup hover events for inline tooltip
        self.setup_pin_tooltip()
    
    def setup_status_bar(self, parent_frame):
        """Create cohesive 3-section status bar"""
        # Main status bar frame - Fixed height for thin status bar
        status_main_frame = customtkinter.CTkFrame(
            parent_frame, 
            fg_color="#333333",  # Dark background for the main frame
            corner_radius=8,
            height=32  # Fixed small height
        )
        status_main_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=8, padx=20)
        status_main_frame.grid_propagate(False)  # Prevent frame from expanding beyond fixed height
        
        # Configure grid weights for equal sections
        status_main_frame.columnconfigure(0, weight=1)
        status_main_frame.columnconfigure(1, weight=0)  # Separator
        status_main_frame.columnconfigure(2, weight=1) 
        status_main_frame.columnconfigure(3, weight=0)  # Separator
        status_main_frame.columnconfigure(4, weight=1)
        # Don't set row weight to prevent vertical expansion
        
        # Section 1: Ready - no vertical expansion
        self.status_section1 = customtkinter.CTkLabel(
            status_main_frame,
            text="▶︎  Ready",
            font=customtkinter.CTkFont(size=11, weight="bold"),  # Smaller font
            text_color="white",
            fg_color="#024A14",  # Dark green
            corner_radius=6,
            anchor="center",
            height=24  # Fixed height
        )
        self.status_section1.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(4, 2), pady=4)  # Only horizontal expansion
        
        # Separator 1 - minimal height
        separator1 = customtkinter.CTkFrame(status_main_frame, fg_color="#CCCCCC", width=1, height=20)
        separator1.grid(row=0, column=1, pady=6)
        
        # Section 2: Events Detection - no vertical expansion  
        self.status_section2 = customtkinter.CTkLabel(
            status_main_frame,
            text="Events Detection",
            font=customtkinter.CTkFont(size=11, weight="bold"),  # Smaller font
            text_color="#AAAAAA",
            fg_color="#444444",  # Grayed out initially
            corner_radius=6,
            anchor="center",
            height=24  # Fixed height
        )
        self.status_section2.grid(row=0, column=2, sticky=(tk.W, tk.E), padx=2, pady=4)  # Only horizontal expansion
        
        # Separator 2 - minimal height
        separator2 = customtkinter.CTkFrame(status_main_frame, fg_color="#CCCCCC", width=1, height=20)
        separator2.grid(row=0, column=3, pady=6)
        
        # Section 3: Status - no vertical expansion
        self.status_section3 = customtkinter.CTkLabel(
            status_main_frame,
            text="Status",
            font=customtkinter.CTkFont(size=11, weight="bold"),  # Smaller font
            text_color="#AAAAAA",
            fg_color="#444444",  # Grayed out initially
            corner_radius=6,
            anchor="center",
            height=24  # Fixed height
        )
        self.status_section3.grid(row=0, column=4, sticky=(tk.W, tk.E), padx=(2, 4), pady=4)  # Only horizontal expansion
        
        # Current status state and flags
        self.current_status_state = "ready"
        self.has_calculated_before = False  # Track if we've calculated before
    
    def set_status_ready(self):
        """Set status to ready state"""
        self.current_status_state = "ready"
        # Section 1: Active (green)
        self.status_section1.configure(fg_color="#024A14", text_color="white")
        
        # Section 2: Grayed out - check if we should show "Events Detection" or reset
        self.status_section2.configure(
            fg_color="#444444", 
            text_color="#AAAAAA",
            text="Events Detection"
        )
        
        # Section 3: Keep calculated state if we've calculated before, otherwise show "Status"
        if self.has_calculated_before:
            # Keep the calculated state visible but ensure correct colors
            pass  # Don't change section 3 if we've calculated before
        else:
            self.status_section3.configure(
                fg_color="#444444", 
                text_color="#AAAAAA",
                text="Status"
            )
    
    def set_status_detecting(self, event_count):
        """Set status to detecting/calculating state"""
        self.current_status_state = "detecting"
        # Section 1: Grayed out
        self.status_section1.configure(fg_color="#444444", text_color="#AAAAAA")
        # Section 2: Active (purple)
        self.status_section2.configure(
            fg_color="#6A36E3", 
            text_color="white",
            text=f"🔎  Detected {event_count} events - Calculating"
        )
        # Section 3: Grayed out or keep previous state
        if self.has_calculated_before:
            # Keep previous calculated state but grayed out
            self.status_section3.configure(fg_color="#444444", text_color="#AAAAAA")
        else:
            self.status_section3.configure(
                fg_color="#444444", 
                text_color="#AAAAAA",
                text="Status"
            )
    
    def set_status_calculated_phase1(self, event_count):
        """Set status to calculated phase 1 (with checkmark for 1 second)"""
        self.current_status_state = "calculated_phase1"
        self.has_calculated_before = True
        
        # Section 1: Grayed out
        self.status_section1.configure(fg_color="#444444", text_color="#AAAAAA")
        # Section 2: Grayed out
        self.status_section2.configure(
            fg_color="#444444", 
            text_color="#AAAAAA",
            text="Events Detection"
        )
        # Section 3: Active (light yellow) with checkmark
        self.status_section3.configure(
            fg_color="#FDF9DC",
            text_color="black", 
            text=f"✅ Calculated! ({event_count} events)"
        )
        
        # Schedule phase 2 after 1 second
        self.root.after(1000, lambda: self.set_status_calculated_phase2(event_count))
    
    def set_status_calculated_phase2(self, event_count):
        """Set status to calculated phase 2 (without checkmark, both Ready and Calculated active)"""
        self.current_status_state = "calculated_phase2"
        
        # Section 1: Back to active (green)
        self.status_section1.configure(fg_color="#024A14", text_color="white")
        # Section 2: Grayed out
        self.status_section2.configure(
            fg_color="#444444", 
            text_color="#AAAAAA",
            text="Events Detection"
        )
        # Section 3: Grayed background with white text, no checkmark
        self.status_section3.configure(
            fg_color="#444444",  # Use grayed background like Events Detection
            text_color="white",  # White text for visibility
            text=f"Calculated! ({event_count} events)"  # No checkmark
        )
    
    def set_status_calculated(self, event_count, total_duration):
        """Set status to calculated state (starts phase 1)"""
        self.set_status_calculated_phase1(event_count)
    
    def toggle_always_on_top(self):
        """Toggle the always-on-top state of the window"""
        self.always_on_top = not self.always_on_top
        
        # Update window attributes
        self.root.attributes('-topmost', self.always_on_top)
        
        # Update button icon
        if self.always_on_top:
            self.always_on_top_btn.configure(image=self.pinned_image)
        else:
            self.always_on_top_btn.configure(image=self.unpinned_image)
    
    def get_clipboard_content(self):
        """Get clipboard content using pbpaste command with robust encoding handling"""
        try:
            # Try UTF-8 first (most common)
            result = subprocess.run(['pbpaste'], capture_output=True, timeout=0.5)
            
            # Try multiple encodings to handle different clipboard formats
            for encoding in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
                try:
                    content = result.stdout.decode(encoding)
                    # Verify it's valid XML by checking for XML declaration
                    if '<?xml' in content:
                        return content
                except (UnicodeDecodeError, AttributeError):
                    continue
            
            # If all encodings fail, try with error replacement
            content = result.stdout.decode('utf-8', errors='replace')
            return content
            
        except Exception as e:
            return None
    
    def has_clipboard_changed(self, clipboard_content):
        """Robust check if clipboard content has changed - detects timing modifications"""
        if not clipboard_content:
            return False
        
        # Use hash of entire content to detect ANY change, including timing modifications
        import hashlib
        current_hash = hashlib.md5(clipboard_content.encode('utf-8')).hexdigest()
        
        # Compare with last known hash
        if not hasattr(self, 'last_clipboard_hash'):
            self.last_clipboard_hash = ""
        
        if current_hash != self.last_clipboard_hash:
            self.last_clipboard_hash = current_hash
            return True
        
        return False
    
    def is_nuendo_xml_content(self, content):
        """Quick validation if content might be Nuendo XML without full parsing"""
        if not content:
            return False
        
        # Fast preliminary checks - more lenient to handle partial clipboard reads
        # Don't require 'filename' as it might not be in truncated/partial clipboard data
        return ('<?xml' in content and 
                ('region' in content or 'vst-xml' in content))
    
    def parse_nuendo_xml(self, xml_content):
        """Parse Nuendo XML to extract clip information with caching"""
        
        # Use cached result if parsing the same content
        if xml_content == self.cached_clipboard_content and self.cached_clips is not None:
            return self.cached_clips
        
        clips = []
        
        try:
            # Quick validation before expensive parsing
            if not self.is_nuendo_xml_content(xml_content):
                return None
            
            # CRITICAL FIX: Remove invalid XML control characters that Cubase/Nuendo sometimes includes
            # Control characters (0x00-0x1F except tab/CR/LF) are not valid in XML
            import re
            # Remove control chars except tab (\x09), LF (\x0A), CR (\x0D)
            xml_content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', xml_content)
            
            # Parse XML using ElementTree
            root = ET.fromstring(xml_content)
            regions = root.findall('.//region')
            
            for region in regions:
                filename_elem = region.find('filename')
                start_elem = region.find('start') 
                end_elem = region.find('end')
                
                if filename_elem is not None and start_elem is not None and end_elem is not None:
                    full_filepath = filename_elem.text
                    filename = full_filepath.split('/')[-1] if full_filepath else "Unknown"
                    start = int(start_elem.text)
                    end = int(end_elem.text)
                    
                    if end > start:
                        clips.append({
                            'filename': filename,
                            'start': start,
                            'end': end,
                            'duration_samples': end - start
                        })
            
            # Cache the result
            self.cached_clipboard_content = xml_content
            self.cached_clips = clips
                        
        except Exception as e:
            # Don't change status for parsing errors, just return None
            return None
            
        return clips
    
    def samples_to_time(self, samples, sample_rate):
        """Convert samples to time format (mm:ss.mmm)"""
        seconds = samples / sample_rate
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        
        return f"{minutes}:{remaining_seconds:02d}.{milliseconds:03d}"
    
    def toggle_details(self):
        """Show or hide the detailed results panel"""
        if self.details_visible.get():
            # Hide details
            self.results_frame.grid_remove()
            self.toggle_details_btn.configure(text="📝 Show Details")  # Fixed: Use configure for CustomTkinter
            self.details_visible.set(False)
            self.root.geometry("600x500")  # Smaller window when details hidden
        else:
            # Show details
            self.results_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
            self.toggle_details_btn.configure(text="📝 Hide Details")  # Fixed: Use configure for CustomTkinter
            self.details_visible.set(True)
            self.root.geometry("600x800")  # Larger window when details shown
    
    def calculate_duration(self, clips=None):
        """Calculate total duration from clipboard content or provided clips"""
        # Get sample rate
        selected_text = self.sample_rate_combo.get()
        if not selected_text:
            messagebox.showerror("Error", "Please select a sample rate")
            return
        
        sample_rate = int(self.rate_mapping[selected_text])
        
        # Save the selected sample rate
        self.config['last_sample_rate'] = str(sample_rate)
        self.save_config()
        
        # Use provided clips or parse from clipboard
        if clips is None:
            # Get clipboard content
            clipboard = self.get_clipboard_content()
            if not clipboard:
                messagebox.showerror("Error", "Could not read clipboard content")
                return
            
            # Parse XML
            clips = self.parse_nuendo_xml(clipboard)
            if not clips:
                messagebox.showwarning("No Data", 
                                     "No valid Cubase/Nuendo clip data found in clipboard.\n" +
                                     "Please copy selected clips from Cubase/Nuendo and try again.")
                return
        
        # Calculate results
        total_samples = sum(clip['duration_samples'] for clip in clips)
        total_duration = self.samples_to_time(total_samples, sample_rate)
        total_seconds = total_samples / sample_rate
        
        # Display BIG result prominently
        big_result_text = f"{total_duration} sec"
        self.big_result_label.config(text=big_result_text)
        
        # Format detailed results 
        result_text = "CUBASE/NUENDO CLIPS ANALYSIS\n"
        result_text += "=" * 60 + "\n\n"
        result_text += f"Found {len(clips)} clips:\n\n"
        
        for i, clip in enumerate(clips, 1):
            duration = self.samples_to_time(clip['duration_samples'], sample_rate)
            duration_seconds = clip['duration_samples'] / sample_rate
            result_text += f"{i}. {clip['filename']}\n"
            result_text += f"   Duration: {duration} ({duration_seconds:.3f}s)\n"
            result_text += f"   Samples: {clip['start']:,} to {clip['end']:,}\n\n"
        
        result_text += "=" * 60 + "\n"
        result_text += f"⌛ TOTAL DURATION: {total_duration}\n"
        result_text += f"📀 Total Samples: {total_samples:,}\n"
        result_text += f"🔊 Sample Rate: {sample_rate:,} Hz\n"
        result_text += "=" * 60 + "\n\n"
        result_text += "✅ Original clipboard data preserved for pasting!\n"
        result_text += f"📋 You can still paste normally in Cubase/Nuendo"
        
        # Update detailed results panel
        self.results_text.config(state=tk.NORMAL)  # Enable editing to insert text
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(1.0, result_text)
        self.results_text.config(state=tk.DISABLED)  # Make read-only again
        
        # Store result for copying
        self.last_result = f"{total_duration}"
        
        # Show the previously hidden button - Centered
        self.toggle_details_btn.grid(row=8, column=0, columnspan=3, pady=(0, 15))  # Centered across all 3 columns
        
        # Update status to calculated
        self.set_status_calculated(len(clips), total_duration)
        
        # Restore original XML data to clipboard to preserve Cubase/Nuendo paste functionality
        if hasattr(self, 'original_clipboard_content') and self.original_clipboard_content:
            try:
                subprocess.run(['pbcopy'], input=self.original_clipboard_content, text=True)
            except:
                pass
    
    def auto_check_clipboard(self):
        """Optimized clipboard monitoring - only responds to Cubase/Nuendo content"""
        clipboard = self.get_clipboard_content()
        
        # Only process if content is potentially from Cubase/Nuendo
        if clipboard and self.is_nuendo_xml_content(clipboard):
            if self.has_clipboard_changed(clipboard):
                # Store original clipboard content for later restoration
                self.original_clipboard_content = clipboard
                
                # Parse once and cache the result
                clips = self.parse_nuendo_xml(clipboard)
                if clips:
                    # Show detecting status
                    self.set_status_detecting(len(clips))
                    
                    # Calculate after a brief moment to show detecting status
                    self.root.after(150, lambda: self.calculate_duration(clips))
                else:
                    # Invalid XML, back to ready
                    self.set_status_ready()
            else:
                # Same valid content - don't interfere with calculated states
                if self.cached_clips:
                    # Only update if we're not in a calculated state
                    if self.current_status_state not in ["calculated_phase1", "calculated_phase2"]:
                        if self.has_calculated_before:
                            # We have results, restore calculated phase 2 state
                            self.set_status_calculated_phase2(len(self.cached_clips))
                else:
                    self.set_status_ready()
        # If clipboard doesn't contain Cubase/Nuendo content, don't change status
        # This prevents status changes when copying other things
        
        # Schedule next check with faster polling for better responsiveness
        self.root.after(300, self.auto_check_clipboard)  # Check every 300ms

def main():
    # Create and run the modern GUI with CustomTkinter
    root = customtkinter.CTk()  # Use CustomTkinter window instead of tk.Tk()
    
    app = NuendoDurationCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()