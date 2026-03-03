# TARDIS Server - Code Review Recommendations

## led_manager.py

### Best Practices
- [ ] 1. **Bare `except` clause** (line 146): `except:` catches everything including `KeyboardInterrupt` and `SystemExit`. Use `except Exception:` instead.
- [ ] 2. **Debug `print` statements** (lines 11, 14, 31, 97): Replace `print()` calls with Python's `logging` module. This gives you log levels, formatting, and the ability to silence output in production.
- [ ] 3. **`print` with space before parenthesis** (line 97): `print ("Section...")` has a style inconsistency — PEP 8 says no space before the opening parenthesis of a function call.
- [ ] 4. **Missing `__len__` on MockNeoPixel** (line 19): If any code ever calls `len(pixels)`, the mock will fail. Consider adding `def __len__(self): return self.num`.
- [ ] 5. **Duplicate functionality**: `fade_to` (line 162) and `fade_to_color` (line 195) do essentially the same thing with slightly different signatures. Consolidate into one method.

### Performance
- [ ] 6. **Per-pixel Python loop for every effect** (lines 101, 155, 190, 252, 289, 320, etc.): Every effect iterates pixel-by-pixel in Python. For large strips (up to 5000 LEDs), consider using `pixels.fill()` where the entire section is one color, or batch operations if the neopixel library supports them.
- [ ] 7. **`preview_count` iterates all 5000 LEDs** (line 498): Even if only 10 LEDs are active, you write all 5000. You could limit the loop to `max(count, self.num_leds)` and only clear up to what's needed.
- [ ] 8. **Lock contention in tight loops** (lines 152, 189, 251, 287): Acquiring/releasing the lock on every step of an animation (e.g., 50 steps in `breath`) adds overhead. Consider holding the lock for the pixel-write + show, but be aware of the trade-off with responsiveness.

### Security
- [ ] 9. **No input validation on section names**: Methods like `set_color`, `pulse`, etc. silently fall back to the full strip range if a section name is invalid (lines 85-87). This could cause unintended behavior — consider raising a `ValueError` for unknown sections.
- [ ] 10. **No bounds checking on color values**: Color tuples are passed directly to the hardware with no validation that values are 0-255. Malformed input could cause unexpected hardware behavior.

---

## scene_manager.py

### Best Practices
- [ ] 11. **`getattr` dispatch without validation** (line 86): `getattr(self.led_manager, action_name)` will call *any* method on `LEDManager`, including private or dangerous ones. Whitelist allowed action names.
- [ ] 12. **Scenes are hardcoded** (lines 7-46): Scene definitions are module-level constants. Consider loading them from a config file (JSON/YAML) so they can be modified without code changes.
- [ ] 13. **Unused import** (line 3): `random` is imported but only used inside `_flash_sections_randomly`. It's fine, but worth noting.

### Security
- [ ] 14. **Arbitrary method execution** (line 86): This is the most significant security concern. If scene definitions ever come from user input (API, config file), an attacker could invoke any method on `LEDManager` (or inherited methods from `object`). Add an explicit allowlist:
    ```python
    ALLOWED_ACTIONS = {"set_color", "turn_on", "turn_off", "pulse", "fade_to", ...}
    ```

### Performance
- [ ] 15. **Blocking execution**: `play_scene` runs synchronously in the calling thread. Long scenes block the API response. Consider running scenes in a background thread with cancellation support.

---

## sound_manager.py

### Security
- [ ] 16. **Command injection risk** (line 52): `file_name` is passed directly to `subprocess.Popen(['play', '-q', sound_path])`. While using a list (not a string) mitigates shell injection, a filename with special characters or path traversal (`../../etc/passwd`) could be problematic. Validate that `file_name` contains no path separators and resolves within `SOUNDS_DIR`:
    ```python
    resolved = os.path.realpath(sound_path)
    if not resolved.startswith(os.path.realpath(SOUNDS_DIR)):
        raise ValueError("Invalid sound file path")
    ```
- [ ] 17. **Directory traversal** (line 43): `os.path.join(SOUNDS_DIR, file_name)` with a `file_name` like `../../../etc/passwd` would escape the sounds directory. This is a real vulnerability if `file_name` comes from API input.

### Best Practices
- [ ] 18. **Relative `SOUNDS_DIR` path** (line 6): `"sounds"` is relative to the working directory, which can vary. Use an absolute path or resolve relative to the module's location.
- [ ] 19. **Use `logging` instead of `print`** (lines 46, 54, 56, 64): Same as the LED manager — use the `logging` module.
- [ ] 20. **No type hints on `play_sound` return** (line 32): Add `-> None` return type annotation for consistency.
- [ ] 21. **Race condition in `stop_sound`/`play_sound`** (lines 41, 52): If called from multiple threads, `stop_sound` and the subsequent `Popen` aren't atomic. Consider adding a `threading.Lock`.

---

## Priority Summary

| Priority | Item | Category |
|----------|------|----------|
| **High** | #14, #16, #17 — Arbitrary method execution & path traversal | Security |
| **High** | #11 — Whitelist allowed scene actions | Security |
| **Medium** | #2, #19 — Replace `print` with `logging` | Best Practice |
| **Medium** | #5 — Consolidate duplicate fade methods | Best Practice |
| **Medium** | #6, #7 — Optimize pixel loops for large strips | Performance |
| **Low** | #1, #3, #4, #18, #20 — Code style & robustness | Best Practice |
