import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import threading
import time
import sys

# Try to import keyboard, but make it optional
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("Warning: keyboard library not available. Hotkeys will be disabled.")

class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("OnlyAutoclicker")
        self.root.geometry("500x550")
        self.root.resizable(True, True)
        self.root.minsize(480, 500)  # Minimum window size
        
        # Variables
        self.is_clicking = False
        self.click_thread = None
        self.hotkey_handlers = []
        self.hotkey_enabled = False
        
        # Hotkey settings (default: F6 for start/stop)
        self.start_stop_hotkey = tk.StringVar(value="f6")
        self.recording_hotkey = None  # Track which hotkey is being recorded
        self.last_recorded_type = None  # Track last recorded hotkey type for success message
        
        # Click settings
        self.click_interval_ms = tk.IntVar(value=100)  # Default: 100 = 1 second
        self.input_mode = tk.StringVar(value="Mouse")  # Mouse or Keyboard
        self.click_type = tk.StringVar(value="Left")
        self.keyboard_key = tk.StringVar(value="space")  # Default keyboard key to press
        self.click_count = tk.StringVar(value="Infinite")
        self.recording_keyboard_key = False  # Track if recording keyboard key
        self.use_current_pos = tk.BooleanVar(value=True)
        self.custom_x = tk.IntVar(value=0)
        self.custom_y = tk.IntVar(value=0)
        # Hotkeys are always enabled if keyboard library is available
        
        # Disable pyautogui failsafe
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0
        
        self.setup_ui()
        if KEYBOARD_AVAILABLE:
            self.setup_hotkeys()
        
    def setup_ui(self):
        # Main frame with scrollable content
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="OnlyAutoclicker", font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 15))
        
        # Create two-column layout
        left_column = ttk.Frame(main_frame)
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_column = ttk.Frame(main_frame)
        right_column.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=(10, 0))
        
        # Click Interval Section
        interval_frame = ttk.LabelFrame(left_column, text="Click Interval (milliseconds)", padding="8")
        interval_frame.pack(fill=tk.X, pady=3)
        
        interval_input_frame = ttk.Frame(interval_frame)
        interval_input_frame.pack(fill=tk.X, pady=3)
        
        ttk.Label(interval_input_frame, text="Interval:").pack(side=tk.LEFT, padx=5)
        self.interval_entry = ttk.Entry(interval_input_frame, textvariable=self.click_interval_ms, width=15)
        self.interval_entry.pack(side=tk.LEFT, padx=5)
        ttk.Label(interval_input_frame, text="ms").pack(side=tk.LEFT, padx=5)
        
        # Helper label showing seconds equivalent - positioned directly under the input box
        converter_frame = ttk.Frame(interval_frame)
        converter_frame.pack(fill=tk.X, pady=(0, 3))
        # Add padding to align with the entry box (label width + padding)
        ttk.Label(converter_frame, text="", width=8).pack(side=tk.LEFT)  # Spacer to align with entry box
        self.interval_info_label = ttk.Label(converter_frame, text="100 = 1.00s delay", 
                                            font=("Arial", 7), foreground="gray")
        self.interval_info_label.pack(side=tk.LEFT, padx=5)
        
        # Update info label when value changes
        self.click_interval_ms.trace_add("write", self.update_interval_info)
        
        # Click Type Section
        type_frame = ttk.LabelFrame(left_column, text="Input Type", padding="8")
        type_frame.pack(fill=tk.X, pady=3)
        
        # Input mode selection (Mouse or Keyboard)
        ttk.Radiobutton(type_frame, text="Mouse", variable=self.input_mode, 
                       value="Mouse", command=self.toggle_input_mode).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(type_frame, text="Keyboard", variable=self.input_mode, 
                       value="Keyboard", command=self.toggle_input_mode).pack(anchor=tk.W, pady=2)
        
        # Container frame to hold both options (maintains consistent height)
        self.options_container = tk.Frame(type_frame, height=75)  # Use tk.Frame for height control
        self.options_container.pack(fill=tk.X, pady=3)
        self.options_container.pack_propagate(False)  # Prevent frame from shrinking
        
        # Mouse options frame
        self.mouse_options_frame = ttk.Frame(self.options_container)
        self.mouse_options_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.mouse_options_frame, text="Mouse Button:", font=("Arial", 9)).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(self.mouse_options_frame, text="Left Click", variable=self.click_type, 
                       value="Left").pack(anchor=tk.W, padx=20, pady=2)
        ttk.Radiobutton(self.mouse_options_frame, text="Right Click", variable=self.click_type, 
                       value="Right").pack(anchor=tk.W, padx=20, pady=2)
        ttk.Radiobutton(self.mouse_options_frame, text="Middle Click", variable=self.click_type, 
                       value="Middle").pack(anchor=tk.W, padx=20, pady=2)
        
        # Keyboard options frame
        self.keyboard_options_frame = ttk.Frame(self.options_container)
        
        keyboard_bind_frame = ttk.Frame(self.keyboard_options_frame)
        keyboard_bind_frame.pack(fill=tk.X, pady=3)
        ttk.Label(keyboard_bind_frame, text="Key to Press:").pack(side=tk.LEFT, padx=5)
        self.keyboard_key_label = ttk.Label(keyboard_bind_frame, text="SPACE", 
                                            font=("Arial", 9, "bold"), 
                                            foreground="blue", width=15)
        self.keyboard_key_label.pack(side=tk.LEFT, padx=5)
        self.keyboard_key_button = ttk.Button(keyboard_bind_frame, text="Change", 
                                             command=self.record_keyboard_key,
                                             width=10)
        self.keyboard_key_button.pack(side=tk.LEFT, padx=5)
        # Success label for keyboard key
        self.keyboard_key_success_label = ttk.Label(keyboard_bind_frame, text="", 
                                                     font=("Arial", 9, "bold"), 
                                                     foreground="green")
        self.keyboard_key_success_label.pack(side=tk.LEFT, padx=5)
        
        # Add spacer to keyboard frame to match mouse frame height visually
        spacer_frame = ttk.Frame(self.keyboard_options_frame)
        spacer_frame.pack(fill=tk.BOTH, expand=True)
        
        # Update keyboard key label when it changes
        self.keyboard_key.trace_add("write", self.update_keyboard_key_label)
        self.update_keyboard_key_label()
        
        # Initially show mouse options, hide keyboard options
        self.toggle_input_mode()
        
        # Click Count Section (moved to right column)
        count_frame = ttk.LabelFrame(right_column, text="Number of Clicks", padding="8")
        count_frame.pack(fill=tk.X, pady=3)
        
        ttk.Radiobutton(count_frame, text="Infinite", variable=self.click_count, 
                       value="Infinite").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(count_frame, text="Custom Amount", variable=self.click_count, 
                       value="Custom", command=self.toggle_count_input).pack(anchor=tk.W, pady=2)
        
        self.count_entry = ttk.Entry(count_frame, width=10, state=tk.DISABLED)
        self.count_entry.pack(anchor=tk.W, pady=2)
        self.custom_count = tk.IntVar(value=100)
        self.count_entry.configure(textvariable=self.custom_count)
        
        # Hotkey Section (moved to right column)
        hotkey_frame = ttk.LabelFrame(right_column, text="Hotkeys", padding="8")
        hotkey_frame.pack(fill=tk.X, pady=3)
        
        if KEYBOARD_AVAILABLE:
            # Start/Stop hotkey configuration
            start_stop_frame = ttk.Frame(hotkey_frame)
            start_stop_frame.pack(fill=tk.X, pady=3)
            ttk.Label(start_stop_frame, text="Start/Stop:").pack(side=tk.LEFT, padx=5)
            self.start_stop_hotkey_label = ttk.Label(start_stop_frame, text="F6", 
                                                     font=("Arial", 9, "bold"), 
                                                     foreground="blue", width=15)
            self.start_stop_hotkey_label.pack(side=tk.LEFT, padx=5)
            self.start_stop_hotkey_button = ttk.Button(start_stop_frame, text="Change", 
                                                       command=lambda: self.record_hotkey("start_stop"),
                                                       width=10)
            self.start_stop_hotkey_button.pack(side=tk.LEFT, padx=5)
            # Success label for start/stop
            self.start_stop_success_label = ttk.Label(start_stop_frame, text="", 
                                                     font=("Arial", 9, "bold"), 
                                                     foreground="green")
            self.start_stop_success_label.pack(side=tk.LEFT, padx=5)
            
            # Update labels when hotkeys change
            self.start_stop_hotkey.trace_add("write", self.update_hotkey_labels)
            self.update_hotkey_labels()
        else:
            ttk.Label(hotkey_frame, text="Hotkeys unavailable (keyboard library not installed)", 
                     font=("Arial", 9), foreground="red").pack(anchor=tk.W, pady=2)
        
        # Click counter (internal use only, not displayed)
        self.click_count_value = 0
        
    def update_interval_info(self, *args):
        """Update the info label showing delay in appropriate unit (seconds/minutes/hours/days/weeks/months/years)"""
        try:
            input_value = self.click_interval_ms.get()
            if input_value > 0:
                # Apply 100:1 ratio: divide by 100 to get seconds
                seconds = input_value / 100.0
                
                # Format based on duration (check from largest to smallest)
                if seconds >= 31536000:  # Years (365 days = 31,536,000 seconds)
                    years = seconds / 31536000.0
                    if years == int(years):
                        self.interval_info_label.config(text=f"{input_value} = {int(years)}year delay")
                    else:
                        self.interval_info_label.config(text=f"{input_value} = {years:.2f}year delay")
                elif seconds >= 2592000:  # Months (30 days = 2,592,000 seconds)
                    months = seconds / 2592000.0
                    if months == int(months):
                        self.interval_info_label.config(text=f"{input_value} = {int(months)}month delay")
                    else:
                        self.interval_info_label.config(text=f"{input_value} = {months:.2f}month delay")
                elif seconds >= 604800:  # Weeks (7 days = 604,800 seconds)
                    weeks = seconds / 604800.0
                    if weeks == int(weeks):
                        self.interval_info_label.config(text=f"{input_value} = {int(weeks)}week delay")
                    else:
                        self.interval_info_label.config(text=f"{input_value} = {weeks:.2f}week delay")
                elif seconds >= 86400:  # Days (86400 seconds = 1 day)
                    days = seconds / 86400.0
                    if days == int(days):
                        self.interval_info_label.config(text=f"{input_value} = {int(days)}day delay")
                    else:
                        self.interval_info_label.config(text=f"{input_value} = {days:.2f}day delay")
                elif seconds >= 3600:  # Hours (3600 seconds = 1 hour)
                    hours = seconds / 3600.0
                    if hours == int(hours):
                        self.interval_info_label.config(text=f"{input_value} = {int(hours)}hr delay")
                    else:
                        self.interval_info_label.config(text=f"{input_value} = {hours:.2f}hr delay")
                elif seconds >= 60:  # Minutes (60 seconds = 1 minute)
                    minutes = seconds / 60.0
                    if minutes == int(minutes):
                        self.interval_info_label.config(text=f"{input_value} = {int(minutes)}min delay")
                    else:
                        self.interval_info_label.config(text=f"{input_value} = {minutes:.2f}min delay")
                else:  # Seconds
                    self.interval_info_label.config(text=f"{input_value} = {seconds:.2f}s delay")
            else:
                self.interval_info_label.config(text="Invalid: must be > 0")
        except:
            pass
        
    def toggle_position_input(self):
        if self.use_current_pos.get():
            self.x_entry.config(state=tk.DISABLED)
            self.y_entry.config(state=tk.DISABLED)
        else:
            self.x_entry.config(state=tk.NORMAL)
            self.y_entry.config(state=tk.NORMAL)
            
    def toggle_count_input(self):
        if self.click_count.get() == "Custom":
            self.count_entry.config(state=tk.NORMAL)
        else:
            self.count_entry.config(state=tk.DISABLED)
    
    def toggle_input_mode(self):
        """Show/hide mouse or keyboard options based on selected input mode"""
        if self.input_mode.get() == "Mouse":
            # Show mouse options, hide keyboard options
            self.mouse_options_frame.pack(fill=tk.BOTH, expand=True)
            self.keyboard_options_frame.pack_forget()
        else:
            # Show keyboard options, hide mouse options
            self.mouse_options_frame.pack_forget()
            self.keyboard_options_frame.pack(fill=tk.BOTH, expand=True)
    
    def update_keyboard_key_label(self, *args):
        """Update the keyboard key display label"""
        try:
            key_name = self.keyboard_key.get().upper()
            self.keyboard_key_label.config(text=key_name)
        except:
            pass
    
    def record_keyboard_key(self):
        """Record a keyboard key to press automatically"""
        if not KEYBOARD_AVAILABLE:
            return
        
        if self.recording_keyboard_key or self.recording_hotkey is not None:
            return
        
        self.recording_keyboard_key = True
        
        # Disable button while recording and clear success message
        self.keyboard_key_button.config(state=tk.DISABLED, text="Press key...")
        self.keyboard_key_success_label.config(text="")
        
        # Use a thread to read the key without blocking the UI
        def read_key_thread():
            try:
                # Temporarily unhook all to avoid conflicts
                keyboard.unhook_all()
                
                # Wait for a key press using read_key (blocks until key is pressed)
                try:
                    key_name = keyboard.read_key().lower()
                    
                    # Cancel if ESC is pressed
                    if key_name == 'esc':
                        self.root.after(0, self.cancel_keyboard_key_recording)
                        return
                    
                    # Validate key name
                    if key_name and key_name != 'unknown':
                        # Update the keyboard key in the main thread
                        self.root.after(0, lambda k=key_name: self.keyboard_key.set(k))
                        
                        # Clean up and show success
                        self.root.after(0, self.finish_keyboard_key_recording)
                    else:
                        self.root.after(0, self.cancel_keyboard_key_recording)
                except Exception as e:
                    print(f"Error reading key: {e}")
                    self.root.after(0, self.cancel_keyboard_key_recording)
            except Exception as e:
                self.root.after(0, self.cancel_keyboard_key_recording)
        
        # Start the key reading thread
        threading.Thread(target=read_key_thread, daemon=True).start()
    
    def finish_keyboard_key_recording(self):
        """Finish keyboard key recording"""
        self.recording_keyboard_key = False
        self.keyboard_key_button.config(state=tk.NORMAL, text="Change")
        
        # Restore hotkeys if they were enabled
        if self.hotkey_enabled_var.get():
            self.setup_hotkeys()
        
        # Show success message with fade effect
        self.show_keyboard_key_success_message()
    
    def show_keyboard_key_success_message(self):
        """Show success message for keyboard key with fade-out effect"""
        label = self.keyboard_key_success_label
        
        # Show "SUCCESS" in green
        label.config(text="SUCCESS", foreground="green")
        
        # Start fade-out animation after 2 seconds
        self.fade_out_success(label, 2000, 0)
    
    def cancel_keyboard_key_recording(self):
        """Cancel keyboard key recording"""
        self.recording_keyboard_key = False
        self.keyboard_key_button.config(state=tk.NORMAL, text="Change")
        
        # Restore hotkeys if they were enabled
        if self.hotkey_enabled_var.get():
            self.setup_hotkeys()
            
    def get_current_position(self):
        try:
            x, y = pyautogui.position()
            self.custom_x.set(x)
            self.custom_y.set(y)
            messagebox.showinfo("Position", f"Current position saved:\nX: {x}, Y: {y}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get position: {str(e)}")
        
    def setup_hotkeys(self):
        """Setup hotkey handlers using keyboard library"""
        if not KEYBOARD_AVAILABLE:
            return
        
        # Clear existing hotkey handlers
        try:
            keyboard.unhook_all()
        except:
            pass
        
        def on_start_stop(event=None):
            if self.is_clicking:
                self.root.after(0, self.stop_clicking)
            else:
                self.root.after(0, self.start_clicking)
        
        try:
            start_stop_key = self.start_stop_hotkey.get().lower()
            
            keyboard.on_press_key(start_stop_key, on_start_stop, suppress=False)
            self.hotkey_handlers = [on_start_stop]
        except Exception as e:
            print(f"Warning: Could not setup hotkeys: {e}")
    
    def update_hotkey_labels(self, *args):
        """Update the hotkey display labels"""
        try:
            start_stop_key = self.start_stop_hotkey.get().upper()
            self.start_stop_hotkey_label.config(text=start_stop_key)
        except:
            pass
    
    def record_hotkey(self, hotkey_type):
        """Record a new hotkey by waiting for user input"""
        if not KEYBOARD_AVAILABLE:
            return
        
        if self.recording_hotkey is not None:
            return
        
        self.recording_hotkey = hotkey_type
        
        # Don't allow recording if keyboard key is being recorded
        if self.recording_keyboard_key:
            return
        
        # Disable button while recording and clear success message
        self.start_stop_hotkey_button.config(state=tk.DISABLED, text="Press key...")
        self.start_stop_success_label.config(text="")
        
        # Use a thread to read the key without blocking the UI
        def read_key_thread():
            try:
                # Temporarily unhook all to avoid conflicts
                keyboard.unhook_all()
                
                # Wait for a key press using read_key (blocks until key is pressed)
                try:
                    key_name = keyboard.read_key().lower()
                    
                    # Cancel if ESC is pressed
                    if key_name == 'esc':
                        self.root.after(0, lambda: self.cancel_hotkey_recording())
                        return
                    
                    # Validate key name
                    if key_name and key_name != 'unknown':
                        # Update the hotkey in the main thread
                        self.root.after(0, lambda k=key_name: self.start_stop_hotkey.set(k))
                        
                        # Clean up and show success
                        self.root.after(0, lambda: self.finish_hotkey_recording("start_stop"))
                    else:
                        self.root.after(0, self.cancel_hotkey_recording)
                except Exception as e:
                    print(f"Error reading key: {e}")
                    self.root.after(0, self.cancel_hotkey_recording)
            except Exception as e:
                self.root.after(0, self.cancel_hotkey_recording)
        
        # Start the key reading thread
        threading.Thread(target=read_key_thread, daemon=True).start()
    
    def finish_hotkey_recording(self, hotkey_type):
        """Finish hotkey recording and restore hotkeys"""
        self.recording_hotkey = None
        self.last_recorded_type = hotkey_type
        self.start_stop_hotkey_button.config(state=tk.NORMAL, text="Change")
        
        # Restore hotkeys
        self.setup_hotkeys()
        
        # Show success message with fade effect
        self.show_success_message(hotkey_type)
    
    def show_success_message(self, hotkey_type):
        """Show success message with fade-out effect"""
        if hotkey_type == "start_stop":
            label = self.start_stop_success_label
        else:
            label = self.stop_success_label
        
        # Show "SUCCESS" in green
        label.config(text="SUCCESS", foreground="green")
        
        # Start fade-out animation after 2 seconds
        self.fade_out_success(label, 2000, 0)
    
    def fade_out_success(self, label, delay_ms, step):
        """Fade out the success message by gradually lightening the green"""
        if delay_ms > 0:
            # Wait 2 seconds before starting fade
            self.root.after(delay_ms, lambda: self.fade_out_success(label, 0, 0))
        else:
            # Fade out over 500ms (10 steps of 50ms each)
            # Gradually change from green to light green to white
            colors = [
                "#00ff00",  # Bright green
                "#00ee00",  # Slightly lighter
                "#00dd00",
                "#00cc00",
                "#00bb00",
                "#00aa00",
                "#009900",
                "#008800",
                "#007700",
                "#006600",
                "#ffffff"   # White (invisible on white background)
            ]
            
            if step < len(colors):
                try:
                    label.config(foreground=colors[step])
                    self.root.after(50, lambda: self.fade_out_success(label, 0, step + 1))
                except:
                    label.config(text="")
            else:
                # Fade complete, hide the label
                label.config(text="")
    
    def cancel_hotkey_recording(self):
        """Cancel hotkey recording"""
        self.recording_hotkey = None
        self.start_stop_hotkey_button.config(state=tk.NORMAL, text="Change")
        
        # Restore hotkeys
        self.setup_hotkeys()
    
    def toggle_hotkeys(self):
        """Hotkeys are always enabled if keyboard library is available"""
        # Hotkeys are always enabled, no toggle needed
        pass
        
    def start_clicking(self):
        if self.is_clicking:
            return
            
        try:
            self.is_clicking = True
            self.click_count_value = 0
            
            # Always use current mouse position (Click Position section removed)
            use_current = True
            click_x = None
            click_y = None
                
            # Validate and get click interval
            try:
                interval_ms = self.click_interval_ms.get()
                if interval_ms <= 0:
                    raise ValueError("Click interval must be greater than 0 milliseconds")
            except (ValueError, tk.TclError):
                messagebox.showerror("Error", "Invalid click interval. Please enter a positive number in milliseconds.")
                self.is_clicking = False
                return
            
            # Get input mode and type
            input_mode = self.input_mode.get()
            click_type = self.click_type.get().lower()
            keyboard_key = self.keyboard_key.get().lower()
            
            # Get click count
            if self.click_count.get() == "Infinite":
                max_clicks = float('inf')
            else:
                try:
                    max_clicks = self.custom_count.get()
                    if max_clicks <= 0:
                        raise ValueError("Click count must be greater than 0")
                except (ValueError, tk.TclError):
                    messagebox.showerror("Error", "Invalid click count. Using infinite.")
                    max_clicks = float('inf')
            
            # Start clicking thread
            self.click_thread = threading.Thread(
                target=self.click_loop, 
                args=(use_current, click_x, click_y, input_mode, click_type, keyboard_key, max_clicks),
                daemon=True
            )
            self.click_thread.start()
        except Exception as e:
            self.is_clicking = False
            messagebox.showerror("Error", f"Failed to start clicking: {str(e)}")
        
    def click_loop(self, use_current_pos, x, y, input_mode, click_type, keyboard_key, max_clicks):
        # Get interval, apply 100:1 ratio (input / 100 = seconds)
        try:
            input_value = self.click_interval_ms.get()
            if input_value <= 0:
                input_value = 100  # Default to 1 second if invalid
            # Apply 100:1 ratio: divide by 100 to get seconds directly
            interval = input_value / 100.0
        except:
            interval = 1.0  # Default to 1 second on error
        count = 0
        
        try:
            while self.is_clicking and count < max_clicks:
                try:
                    # Perform the action based on input mode
                    if input_mode == "Keyboard":
                        # Press keyboard key
                        if KEYBOARD_AVAILABLE:
                            keyboard.press_and_release(keyboard_key)
                        else:
                            raise Exception("Keyboard library not available")
                    else:
                        # Perform mouse click
                        if use_current_pos:
                            # Click at current mouse position without moving it
                            if click_type == "left":
                                pyautogui.click()  # Clicks at current mouse position
                            elif click_type == "right":
                                pyautogui.rightClick()  # Clicks at current mouse position
                            elif click_type == "middle":
                                pyautogui.middleClick()  # Clicks at current mouse position
                            else:
                                pyautogui.click()  # Default to left
                        else:
                            # Click at fixed coordinates
                            if click_type == "left":
                                pyautogui.click(x, y)
                            elif click_type == "right":
                                pyautogui.rightClick(x, y)
                            elif click_type == "middle":
                                pyautogui.middleClick(x, y)
                            else:
                                pyautogui.click(x, y)  # Default to left
                        
                    count += 1
                    self.click_count_value = count
                    
                    time.sleep(interval)
                except Exception as e:
                    error_msg = f"Clicking error: {str(e)}"
                    try:
                        self.root.after(0, lambda msg=error_msg: messagebox.showerror("Error", msg))
                    except:
                        pass
                    break
        except Exception as e:
            error_msg = f"Loop error: {str(e)}"
            try:
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("Error", msg))
            except:
                pass
        finally:
            try:
                self.root.after(0, self.stop_clicking)
            except:
                pass
        
    def stop_clicking(self):
        if not self.is_clicking:
            return
            
        try:
            self.is_clicking = False
        except:
            pass
        
    def on_closing(self):
        try:
            self.is_clicking = False
            if KEYBOARD_AVAILABLE:
                keyboard.unhook_all()
        except:
            pass
        self.root.destroy()
        sys.exit()

def main():
    try:
        root = tk.Tk()
        app = AutoClicker(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Fatal Error", f"Application failed to start: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
